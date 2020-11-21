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
    def button_validate(self):
        res = super(Picking, self).button_validate()
        if not self.env.user.email:
            raise UserError(_('You must have an email address in your User Preferences to send emails.'))
 
        if self.picking_type_id.is_rental_picking or self.picking_type_id.return_picking_type_id.is_rental_picking:
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
                        line.lot_id.write({'state': 'rent'})
        return True
    
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
        
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
