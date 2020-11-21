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
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare
from datetime import datetime


class Picking(models.Model):
    _inherit = "stock.picking"
    
    @api.model
    def default_get(self, field_list):
        res = super(Picking, self).default_get(field_list)
        res.update({
            'date_done': datetime.now(),
        })
        return res

    
    @api.multi
    def action_done(self):
        eff_date = self.date_done
        res = super(Picking, self).action_done()
        self.write({'date_done': eff_date})
        return res
    
    @api.model
    def create(self, vals):
        res = super(Picking, self).create(vals)
        res.scheduled_date = res.date_done or False
        return res
    
    @api.multi
    def write(self, vals):
        if 'date_done' in vals and vals['date_done']:
            vals['scheduled_date'] = vals['date_done']
        res = super(Picking, self).write(vals)
        if 'date_done' in vals and vals['date_done']:
            self.move_ids_without_package.update({'date': vals['date_done']})
        return res
        
    @api.multi
    def button_validate(self):
        self.move_ids_without_package.update({'date': self.date_done})
        res = super(Picking, self).button_validate()
        return res
                                        
        
#         """Changes picking state to done by processing the Stock Moves of the Picking
# 
#         Normally that happens when the button "Done" is pressed on a Picking view.
#         @return: True
#         """
#         # TDE FIXME: remove decorator when migration the remaining
#         todo_moves = self.mapped('move_lines').filtered(lambda self: self.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed'])
#         # Check if there are ops not linked to moves yet
#         for pick in self:
#             # # Explode manually added packages
#             # for ops in pick.move_line_ids.filtered(lambda x: not x.move_id and not x.product_id):
#             #     for quant in ops.package_id.quant_ids: #Or use get_content for multiple levels
#             #         self.move_line_ids.create({'product_id': quant.product_id.id,
#             #                                    'package_id': quant.package_id.id,
#             #                                    'result_package_id': ops.result_package_id,
#             #                                    'lot_id': quant.lot_id.id,
#             #                                    'owner_id': quant.owner_id.id,
#             #                                    'product_uom_id': quant.product_id.uom_id.id,
#             #                                    'product_qty': quant.qty,
#             #                                    'qty_done': quant.qty,
#             #                                    'location_id': quant.location_id.id, # Could be ops too
#             #                                    'location_dest_id': ops.location_dest_id.id,
#             #                                    'picking_id': pick.id
#             #                                    }) # Might change first element
#             # # Link existing moves or add moves when no one is related
#             for ops in pick.move_line_ids.filtered(lambda x: not x.move_id):
#                 # Search move with this product
#                 moves = pick.move_lines.filtered(lambda x: x.product_id == ops.product_id)
#                 moves = sorted(moves, key=lambda m: m.quantity_done < m.product_qty, reverse=True)
#                 if moves:
#                     ops.move_id = moves[0].id
#                 else:
#                     new_move = self.env['stock.move'].create({
#                                                     'name': _('New Move:') + ops.product_id.display_name,
#                                                     'product_id': ops.product_id.id,
#                                                     'product_uom_qty': ops.qty_done,
#                                                     'product_uom': ops.product_uom_id.id,
#                                                     'location_id': pick.location_id.id,
#                                                     'location_dest_id': pick.location_dest_id.id,
#                                                     'picking_id': pick.id,
#                                                     'picking_type_id': pick.picking_type_id.id,
#                                                    })
#                     ops.move_id = new_move.id
#                     new_move._action_confirm()
#                     todo_moves |= new_move
#                     #'qty_done': ops.qty_done})
#         todo_moves._action_done()
# #         self.write({'date_done': fields.Datetime.now()})
#         return True
    
    
class StockMove(models.Model):
    _inherit = "stock.move"


    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id):
        self.ensure_one()
        AccountMove = self.env['account.move']
        quantity = self.env.context.get('forced_quantity', self.product_qty)
        quantity = quantity if self._is_in() else -1 * quantity

        # Make an informative `ref` on the created account move to differentiate between classic
        # movements, vacuum and edition of past moves.
        ref = self.picking_id.name
        if self.env.context.get('force_valuation_amount'):
            if self.env.context.get('forced_quantity') == 0:
                ref = 'Revaluation of %s (negative inventory)' % ref
            elif self.env.context.get('forced_quantity') is not None:
                ref = 'Correction of %s (modification of past move)' % ref

        move_lines = self.with_context(forced_ref=ref)._prepare_account_move_line(quantity, abs(self.value), credit_account_id, debit_account_id)
        if move_lines:
            date = self.picking_id.date_done
            if not date:
                date = self._context.get('force_period_date', fields.Date.context_today(self))
            new_account_move = AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': ref,
                'stock_move_id': self.id,
            })
            new_account_move.post()

    def _account_entry_move(self):
        """ Accounting Valuation Entries """
        self.ensure_one()
#         if self.product_id.type != 'product':
        if self.product_id.type not in ['product', 'consu']:
            # no stock valuation for consumable products
            return False
        if self.restrict_partner_id:
            # if the move isn't owned by the company, we don't make any valuation
            return False

        location_from = self.location_id
        location_to = self.location_dest_id
        company_from = self.mapped('move_line_ids.location_id.company_id') if self._is_out() else False
        company_to = self.mapped('move_line_ids.location_dest_id.company_id') if self._is_in() else False

        # Create Journal Entry for products arriving in the company; in case of routes making the link between several
        # warehouse of the same company, the transit location belongs to this company, so we don't need to create accounting entries
        if self._is_in():
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if location_from and location_from.usage == 'customer':  # goods returned from customer
                self.with_context(force_company=company_to.id)._create_account_move_line(acc_dest, acc_valuation, journal_id)
            else:
                self.with_context(force_company=company_to.id)._create_account_move_line(acc_src, acc_valuation, journal_id)

        # Create Journal Entry for products leaving the company
        if self._is_out():
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if location_to and location_to.usage == 'supplier':  # goods returned to supplier
                self.with_context(force_company=company_from.id)._create_account_move_line(acc_valuation, acc_src, journal_id)
            else:
                self.with_context(force_company=company_from.id)._create_account_move_line(acc_valuation, acc_dest, journal_id)

        if self.company_id.anglo_saxon_accounting:
            # Creates an account entry from stock_input to stock_output on a dropship move. https://github.com/odoo/odoo/issues/12687
            journal_id, acc_src, acc_dest, acc_valuation = self._get_accounting_data_for_valuation()
            if self._is_dropshipped():
                self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_src, acc_dest, journal_id)
            elif self._is_dropshipped_returned():
                self.with_context(force_company=self.company_id.id)._create_account_move_line(acc_dest, acc_src, journal_id)

        if self.company_id.anglo_saxon_accounting:
            #eventually reconcile together the invoice and valuation accounting entries on the stock interim accounts
            allowed_invoice_types = self._is_in() and ('in_invoice', 'out_refund') or ('in_refund', 'out_invoice')
            self._get_related_invoices().filtered(lambda x: x.type in allowed_invoice_types)._anglo_saxon_reconcile_valuation(product=self.product_id)
    
    
    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super(StockMove, self)._prepare_move_line_vals(quantity, reserved_quant)
        if self.date:
            vals.update({'date': self.date})
        return vals
    
    
class StockMoveLine(models.Model):
    _inherit = "stock.move.line"   
    
    def _action_done(self):
        res = super(StockMoveLine, self)._action_done()
        for line in self:
            line.write({'date': line.move_id.date})
        return res
        
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
