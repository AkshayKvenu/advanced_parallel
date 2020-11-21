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


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def button_validate(self):
        res = super(Picking, self).button_validate()
#         product_obj=self.move_ids_without_package.product_id.inspection_type_ids.ids
#         for line in self.move_ids_without_package.move_line_ids:
#             print("lineeeeeeeeeeee",line.mapped('inspetion_ids'))
# #         print("resssssssssssssss",product_obj,self.move_ids_without_package.move_line_ids.inspetion_ids)
        if not self.env.user.email:
            raise UserError(_('You must have an email address in your User Preferences to send emails.'))
 
        template = self.env.ref('advanced_lines_sale.email_template_description_user')
        lang = self.env.user.lang
         
         
        if template:
            template.with_context(lang=lang).send_mail(self.id, force_send=True)
        else:
            _logger.warning("No email template found for sending email to the portal user")
 
        return res

    @api.multi
    def action_done(self):
        res = super(Picking, self).action_done()
        if self.picking_type_id.code == 'outgoing':
            for move in self.move_ids_without_package:
                if move.sale_line_id and move.sale_line_id.sale_type == 'rent' and move.sale_line_id.project_id:
                    for line in move.move_line_ids:
                        task = move.sale_line_id._timesheet_create_task(move.sale_line_id.project_id)
                        task.write({
                            'name': move.product_id.name +'[' + line.lot_id.name + ']',
                            'product_id': move.product_id.id,
                            'lot_id': line.lot_id.id,
                            'stock_move_line_id': line.id,
                            'state': 'rent',
                        })
        return res
    
    def _get_overprocessed_stock_moves(self):
        self.ensure_one()
        overprocessed_stock_move = self.move_lines.filtered(
            lambda move: move.product_uom_qty != 0 and float_compare(move.quantity_done, move.product_uom_qty,
                                                                     precision_rounding=move.product_uom.rounding) == 1
        )
        if overprocessed_stock_move:
            raise ValidationError(_("You cannot add more than what was initially planned for the product."))
        return overprocessed_stock_move
    

class StockRule(models.Model):
    _inherit = 'stock.rule'
    
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        res = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
        if res.get('sale_line_id'):
            sale_id = self.env['sale.order.line'].browse(res.get('sale_line_id')).order_id
            if sale_id.sale_type == 'rent':
                rental_picking_type = self.env['stock.picking.type'].search([('is_rental_picking', '=', True)], limit=1)
                if not rental_picking_type:
                    raise UserError(_("No Picking Type defined for Rental Order."))
                res['picking_type_id'] = rental_picking_type.id
            return res 


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    is_rental_picking = fields.Boolean('Rental Picking')
    
    
class RentalNumber(models.Model):
    _inherit = "stock.production.lot"

    is_rental = fields.Boolean('Is Rental', related="product_id.is_rental")
    state = fields.Selection([('rent', 'On Rent'), ('maintenance', 'Under Maintenance'), ('inspection', 'Under Inspection'), ('ready', 'Ready for Mobilization'), ('demobilize', 'Demobilized')], 'Status')
    

class StockMove(models.Model):
    _inherit = "stock.move"


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
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
