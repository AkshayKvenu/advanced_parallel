# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 Amzsys IT Solutions Pvt Ltd
#    (http://www.amzsys.com)
#    info@amzsys.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class AccountVoucherLine(models.Model):
    _inherit = 'account.voucher.line'
    
    partner_id = fields.Many2one('res.partner', 'Partner')
    
    

class AccountVoucher(models.Model):
    _inherit = 'account.voucher'
    
    
#     @api.multi
#     def voucher_move_line_create0(self, line_total, move_id, company_currency, current_currency):
#         import pdb;pdb.set_trace()
#         for line in self.line_ids:
#             #create one move line per voucher line where amount is not 0.0
#             if not line.price_subtotal:
#                 continue
#             line_subtotal = line.price_subtotal
#             if self.voucher_type == 'sale':
#                 line_subtotal = -1 * line.price_subtotal
#             # convert the amount set on the voucher line into the currency of the voucher's company
#             # this calls res_curreny.compute() with the right context,
#             # so that it will take either the rate on the voucher if it is relevant or will use the default behaviour
#             amount = self._convert(line.price_unit*line.quantity)
#             
#             move_line = {
#                 'journal_id': self.journal_id.id,
#                 'name': line.name or '/',
#                 'account_id': line.account_id.id,
#                 'move_id': move_id,
#                 'partner_id': line.partner_id.id or self.partner_id.commercial_partner_id.id,
#                 'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
#                 'quantity': 1,
#                 'credit': abs(amount) if (self.voucher_type == 'sale' and amount > 0.0) or (self.voucher_type == 'purchase' and amount < 0.0) else 0.0,
#                 'debit': abs(amount) if (self.voucher_type == 'purchase' and amount > 0.0) or (self.voucher_type == 'sale' and amount < 0.0) else 0.0,
#                 'date': self.account_date,
#                 'tax_ids': [(4,t.id) for t in line.tax_ids],
#                 'amount_currency': line_subtotal if current_currency != company_currency else 0.0,
#                 'currency_id': company_currency != current_currency and current_currency or False,
#                 'payment_id': self._context.get('payment_id'),
#             }
#             self.env['account.move.line'].with_context(apply_taxes=True).create(move_line)
#         return line_total

    @api.multi
    def voucher_move_line_create(self, line_total, move_id, company_currency, current_currency):
        '''
        Create one account move line, on the given account move, per voucher line where amount is not 0.0.
        It returns Tuple with tot_line what is total of difference between debit and credit and
        a list of lists with ids to be reconciled with this format (total_deb_cred,list_of_lists).

        :param voucher_id: Voucher id what we are working with
        :param line_total: Amount of the first line, which correspond to the amount we should totally split among all voucher lines.
        :param move_id: Account move wher those lines will be joined.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: Tuple build as (remaining amount not allocated on voucher lines, list of account_move_line created in this method)
        :rtype: tuple(float, list of int)
        '''
        tax_calculation_rounding_method = self.env.user.company_id.tax_calculation_rounding_method
        tax_lines_vals = []
        for line in self.line_ids:
            #create one move line per voucher line where amount is not 0.0
            if not line.price_subtotal:
                continue
            line_subtotal = line.price_subtotal
            if self.voucher_type == 'sale':
                line_subtotal = -1 * line.price_subtotal
            # convert the amount set on the voucher line into the currency of the voucher's company
            amount = self._convert(line.price_unit*line.quantity)
            move_line = {
                'journal_id': self.journal_id.id,
                'name': line.name or '/',
                'account_id': line.account_id.id,
                'move_id': move_id,
                'quantity': line.quantity,
                'product_id': line.product_id.id,
                'partner_id': line.partner_id.id or self.partner_id.commercial_partner_id.id,
                'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                'credit': amount if self.voucher_type == 'sale' else 0.0,
                'debit': amount if self.voucher_type == 'purchase' else 0.0,
                'date': self.account_date,
                'tax_ids': [(4,t.id) for t in line.tax_ids],
                'amount_currency': line_subtotal if current_currency != company_currency else 0.0,
                'currency_id': company_currency != current_currency and current_currency or False,
                'payment_id': self._context.get('payment_id'),
            }
            # Create one line per tax and fix debit-credit for the move line if there are tax included
            if (line.tax_ids and tax_calculation_rounding_method == 'round_per_line'):
                tax_group = line.tax_ids.compute_all(self._convert(line.price_unit), self.company_id.currency_id, line.quantity, line.product_id, self.partner_id)
                if move_line['debit']: move_line['debit'] = tax_group['total_excluded']
                if move_line['credit']: move_line['credit'] = tax_group['total_excluded']
                Currency = self.env['res.currency']
                company_cur = Currency.browse(company_currency)
                current_cur = Currency.browse(current_currency)
                for tax_vals in tax_group['taxes']:
                    if tax_vals['amount']:
                        tax = self.env['account.tax'].browse([tax_vals['id']])
                        account_id = (amount > 0 and tax_vals['account_id'] or tax_vals['refund_account_id'])
                        if not account_id: account_id = line.account_id.id
                        temp = {
                            'account_id': account_id,
                            'name': line.name + ' ' + tax_vals['name'],
                            'tax_line_id': tax_vals['id'],
                            'move_id': move_id,
                            'date': self.account_date,
                            'partner_id': self.partner_id.id,
                            'debit': self.voucher_type != 'sale' and tax_vals['amount'] or 0.0,
                            'credit': self.voucher_type == 'sale' and tax_vals['amount'] or 0.0,
                            'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                        }
                        if company_currency != current_currency:
                            ctx = {}
                            sign = temp['credit'] and -1 or 1
                            amount_currency = company_cur._convert(tax_vals['amount'], current_cur, line.company_id,
                                                 self.account_date or fields.Date.today(), round=True)
                            if self.account_date:
                                ctx['date'] = self.account_date
                            temp['currency_id'] = current_currency
                            temp['amount_currency'] = sign * abs(amount_currency)
                        if temp['debit']<0.0:temp['debit'],temp['credit'] =  0.0,-1*temp['debit']
                        if temp['credit']<0.0:temp['credit'],temp['debit'] = 0.0,-1*temp['credit']
                        self.env['account.move.line'].create(temp)

            # When global rounding is activated, we must wait until all tax lines are computed to
            # merge them.
            if tax_calculation_rounding_method == 'round_globally':
                # _apply_taxes modifies the dict move_line in place to account for included/excluded taxes
                tax_lines_vals += self.env['account.move.line'].with_context(round=False)._apply_taxes(
                    move_line,
                    move_line.get('debit', 0.0) - move_line.get('credit', 0.0)
                )
                # rounding False means the move_line's amount are not rounded
                currency = self.env['res.currency'].browse(company_currency)
                move_line['debit'] = currency.round(move_line['debit'])
                move_line['credit'] = currency.round(move_line['credit'])
            if move_line['debit']<0.0:move_line['debit'],move_line['credit'] = 0.0,-1*move_line['debit']
            if move_line['credit']<0.0:move_line['credit'],move_line['debit'] = 0.0,-1*move_line['credit']
            self.env['account.move.line'].create(move_line)

        # When round globally is set, we merge the tax lines
        if tax_calculation_rounding_method == 'round_globally':
            tax_lines_vals_merged = {}
            for tax_line_vals in tax_lines_vals:
                key = (
                    tax_line_vals['tax_line_id'],
                    tax_line_vals['account_id'],
                    tax_line_vals['analytic_account_id'],
                )
                if key not in tax_lines_vals_merged:
                    tax_lines_vals_merged[key] = tax_line_vals
                else:
                    tax_lines_vals_merged[key]['debit'] += tax_line_vals['debit']
                    tax_lines_vals_merged[key]['credit'] += tax_line_vals['credit']
            currency = self.env['res.currency'].browse(company_currency)
            for vals in tax_lines_vals_merged.values():
                vals['debit'] = currency.round(vals['debit'])
                vals['credit'] = currency.round(vals['credit'])
                self.env['account.move.line'].create(vals)
        return line_total
    
    @api.multi
    def first_move_line_get(self, move_id, company_currency, current_currency):
        debit = credit = 0.0
        if self.voucher_type == 'purchase':
            credit = self._convert(self.amount)
        elif self.voucher_type == 'sale':
            debit = self._convert(self.amount)
        if debit < 0.0: debit, credit = 0.0, -1 *debit
        if credit < 0.0: debit, credit = -1 * credit, 0.0
        sign = debit - credit < 0 and -1 or 1
        #set the first line of the voucher
        move_line = {
                'name': self.name or '/',
                'debit': debit,
                'credit': credit,
                'account_id': self.account_id.id,
                'move_id': move_id,
                'journal_id': self.journal_id.id,
                'partner_id': self.partner_id.commercial_partner_id.id,
                'currency_id': company_currency != current_currency and current_currency or False,
                'amount_currency': (sign * abs(self.amount)  # amount < 0 for refunds
                    if company_currency != current_currency else 0.0),
                'date': self.account_date,
                'date_maturity': self.date_due,
                'payment_id': self._context.get('payment_id'),
            }
        return move_line


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    
    @api.depends('move_id.line_ids', 'move_id.line_ids.tax_line_id', 'move_id.line_ids.debit', 'move_id.line_ids.credit')
    def _compute_tax_base_amount(self):
        for move_line in self:
            if move_line.tax_line_id:
                print ("Context : ", self._context)
                if 'voucher_type' in self.env.context:
                    move_line.tax_base_amount = abs(move_line.balance * 100 / move_line.tax_line_id.amount)
                else:
                    base_lines = move_line.move_id.line_ids.filtered(lambda line: move_line.tax_line_id in line.tax_ids and move_line.partner_id == line.partner_id)
                    move_line.tax_base_amount = abs(sum(base_lines.mapped('balance')))
            else:
                move_line.tax_base_amount = 0

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

    