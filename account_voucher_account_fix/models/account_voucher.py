# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) © 2019 KITE.
# (http://kite.com.sa)
# info@kite.com.sa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see .
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'
    
#     operating_unit_id = fields.Many2one('operating.unit', string='Operating Unit')
            
    @api.model
    def default_get(self,default_fields):
        res = super(AccountVoucher, self).default_get(default_fields)
        res.update({'pay_now': 'pay_now'})
        return res
    
    @api.onchange('payment_journal_id')
    def _set_payment_journal_account(self):
        if self.payment_journal_id:
            self.journal_id = self.payment_journal_id.id
            if self.voucher_type == 'sale':
                self.account_id = self.payment_journal_id.default_debit_account_id.id
            else:
                self.account_id = self.payment_journal_id.default_credit_account_id.id
                
#     @api.multi
#     def first_move_line_get(self, move_id, company_currency, current_currency):
#         move_line = super(AccountVoucher, self).first_move_line_get(move_id, company_currency, current_currency)
#         move_line['operating_unit_id'] = self.operating_unit_id.id
#         return move_line
                
#     @api.multi
#     def voucher_move_line_create(self, line_total, move_id, company_currency, current_currency):
#         tax_calculation_rounding_method = self.env.user.company_id.tax_calculation_rounding_method
#         tax_lines_vals = []
#         for line in self.line_ids:
#             #create one move line per voucher line where amount is not 0.0
#             if not line.price_subtotal:
#                 continue
#             line_subtotal = line.price_subtotal
#             if self.voucher_type == 'sale':
#                 line_subtotal = -1 * line.price_subtotal
#             # convert the amount set on the voucher line into the currency of the voucher's company
#             amount = self._convert(line.price_unit*line.quantity)
#             move_line = {
#                 'journal_id': self.journal_id.id,
#                 'name': line.name or '/',
#                 'account_id': line.account_id.id,
#                 'move_id': move_id,
#                 'quantity': line.quantity,
#                 'product_id': line.product_id.id,
#                 'partner_id': self.partner_id.commercial_partner_id.id,
#                 'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
#                 'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
#                 'credit': abs(amount) if self.voucher_type == 'sale' else 0.0,
#                 'debit': abs(amount) if self.voucher_type == 'purchase' else 0.0,
#                 'date': self.account_date,
#                 'tax_ids': [(4,t.id) for t in line.tax_ids],
#                 'amount_currency': line_subtotal if current_currency != company_currency else 0.0,
#                 'currency_id': company_currency != current_currency and current_currency or False,
#                 'payment_id': self._context.get('payment_id'),
#                 'operating_unit_id': self.operating_unit_id.id,
#             }
#             # Create one line per tax and fix debit-credit for the move line if there are tax included
#             if (line.tax_ids and tax_calculation_rounding_method == 'round_per_line'):
#                 tax_group = line.tax_ids.compute_all(self._convert(line.price_unit), self.company_id.currency_id, line.quantity, line.product_id, self.partner_id)
#                 if move_line['debit']: move_line['debit'] = tax_group['total_excluded']
#                 if move_line['credit']: move_line['credit'] = tax_group['total_excluded']
#                 Currency = self.env['res.currency']
#                 company_cur = Currency.browse(company_currency)
#                 current_cur = Currency.browse(current_currency)
#                 for tax_vals in tax_group['taxes']:
#                     if tax_vals['amount']:
#                         tax = self.env['account.tax'].browse([tax_vals['id']])
#                         account_id = (amount > 0 and tax_vals['account_id'] or tax_vals['refund_account_id'])
#                         if not account_id: account_id = line.account_id.id
#                         temp = {
#                             'account_id': account_id,
#                             'name': line.name + ' ' + tax_vals['name'],
#                             'tax_line_id': tax_vals['id'],
#                             'move_id': move_id,
#                             'date': self.account_date,
#                             'partner_id': self.partner_id.id,
#                             'debit': self.voucher_type != 'sale' and tax_vals['amount'] or 0.0,
#                             'credit': self.voucher_type == 'sale' and tax_vals['amount'] or 0.0,
#                             'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
#                             'operating_unit_id': self.operating_unit_id.id,
#                         }
#                         if company_currency != current_currency:
#                             ctx = {}
#                             sign = temp['credit'] and -1 or 1
#                             amount_currency = company_cur._convert(tax_vals['amount'], current_cur, line.company_id,
#                                                  self.account_date or fields.Date.today(), round=True)
#                             if self.account_date:
#                                 ctx['date'] = self.account_date
#                             temp['currency_id'] = current_currency
#                             temp['amount_currency'] = sign * abs(amount_currency)
#                         self.env['account.move.line'].create(temp)
# 
#             # When global rounding is activated, we must wait until all tax lines are computed to
#             # merge them.
#             if tax_calculation_rounding_method == 'round_globally':
#                 # _apply_taxes modifies the dict move_line in place to account for included/excluded taxes
#                 tax_lines_vals += self.env['account.move.line'].with_context(round=False)._apply_taxes(
#                     move_line,
#                     move_line.get('debit', 0.0) - move_line.get('credit', 0.0)
#                 )
#                 # rounding False means the move_line's amount are not rounded
#                 currency = self.env['res.currency'].browse(company_currency)
#                 move_line['debit'] = currency.round(move_line['debit'])
#                 move_line['credit'] = currency.round(move_line['credit'])
#                 move_line['operating_unit_id'] = self.operating_unit_id.id
#             self.env['account.move.line'].create(move_line)
# 
#         # When round globally is set, we merge the tax lines
#         if tax_calculation_rounding_method == 'round_globally':
#             tax_lines_vals_merged = {}
#             for tax_line_vals in tax_lines_vals:
#                 key = (
#                     tax_line_vals['tax_line_id'],
#                     tax_line_vals['account_id'],
#                     tax_line_vals['analytic_account_id'],
#                 )
#                 if key not in tax_lines_vals_merged:
#                     tax_lines_vals_merged[key] = tax_line_vals
#                 else:
#                     tax_lines_vals_merged[key]['debit'] += tax_line_vals['debit']
#                     tax_lines_vals_merged[key]['credit'] += tax_line_vals['credit']
#             currency = self.env['res.currency'].browse(company_currency)
#             for vals in tax_lines_vals_merged.values():
#                 vals['debit'] = currency.round(vals['debit'])
#                 vals['credit'] = currency.round(vals['credit'])
#                 vals['operating_unit_id'] = self.operating_unit_id.id
#                 self.env['account.move.line'].create(vals)
#         return line_total
        
    
    # Blocking the creation of Payment from Voucher
    @api.multi
    def action_move_line_create(self):
        '''
        Confirm the vouchers given in ids and create the journal entries for each of them
        '''
        for voucher in self:
            local_context = dict(self._context, force_company=voucher.journal_id.company_id.id)
            if voucher.move_id:
                continue
            company_currency = voucher.journal_id.company_id.currency_id.id
            current_currency = voucher.currency_id.id or company_currency
            # we select the context to use accordingly if it's a multicurrency case or not
            # But for the operations made by _convert, we always need to give the date in the context
            ctx = local_context.copy()
            ctx['date'] = voucher.account_date
            ctx['check_move_validity'] = False
            # Create the account move record.
            move = self.env['account.move'].create(voucher.account_move_get())
            # Get the name of the account_move just created
            # Create the first line of the voucher
            move_line = self.env['account.move.line'].with_context(ctx).create(voucher.with_context(ctx).first_move_line_get(move.id, company_currency, current_currency))
            line_total = move_line.debit - move_line.credit
            if voucher.voucher_type == 'sale':
                line_total = line_total - voucher._convert(voucher.tax_amount)
            elif voucher.voucher_type == 'purchase':
                line_total = line_total + voucher._convert(voucher.tax_amount)
            # Create one move line per voucher line where amount is not 0.0
            line_total = voucher.with_context(ctx).voucher_move_line_create(line_total, move.id, company_currency, current_currency)

            # Create a payment to allow the reconciliation when pay_now = 'pay_now'.
#             if voucher.pay_now == 'pay_now':
#                 payment_id = (self.env['account.payment']
#                     .with_context(force_counterpart_account=voucher.account_id.id)
#                     .create(voucher.voucher_pay_now_payment_create()))
#                 payment_id.post()
# 
#                 # Reconcile the receipt with the payment
#                 lines_to_reconcile = (payment_id.move_line_ids + move.line_ids).filtered(lambda l: l.account_id == voucher.account_id)
#                 lines_to_reconcile.reconcile()

            # Add tax correction to move line if any tax correction specified
            if voucher.tax_correction != 0.0:
                tax_move_line = self.env['account.move.line'].search([('move_id', '=', move.id), ('tax_line_id', '!=', False)], limit=1)
                if len(tax_move_line):
                    tax_move_line.write({'debit': tax_move_line.debit + voucher.tax_correction if tax_move_line.debit > 0 else 0,
                        'credit': tax_move_line.credit + voucher.tax_correction if tax_move_line.credit > 0 else 0})

            # We post the voucher.
            voucher.write({
                'move_id': move.id,
                'state': 'posted',
                'number': move.name
            })
            move.post()
        return True
    
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: