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
from datetime import date
from odoo.exceptions import UserError


class MoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    inspection_ids = fields.Many2many('equipment.inspection', 'move_line_inspection_rel', 'move_line_id', 'inspection_id', 
                                     string="Inspections", domain="[('lot_id', '=', lot_id), ('state', '=', 'valid')]") 
    
    @api.onchange('lot_id')
    def _change_lot_clear_inspection(self):
        self.inspection_ids = False
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    is_rental_type = fields.Boolean('Rental Type', related="picking_type_id.is_rental_picking")
    
    
class Picking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def button_validate(self):
        move_ids = self.move_ids_without_package
        for move in move_ids:
            product_inspection_type_ids = move.mapped('product_id.inspection_type_ids').ids
            for line in move.move_line_ids:
                if not all(t_id in line.mapped('inspection_ids.inspection_type_id').ids for t_id in product_inspection_type_ids):
                    raise UserError(_("You should choose all Inspections with types configured in Product."))
        res = super(Picking, self).button_validate()
        return res

        
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: