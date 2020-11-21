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
    
    delivery_note = fields.Char(string = "Delivery Note")
    
    
    @api.multi
    def _check_duplicate_delivery_note(self):
        for picking in self:
            if picking.picking_type_id.code == 'incoming' and picking.delivery_note:
                if self.search([('picking_type_code', '=', picking.picking_type_id.code), ('delivery_note', '=', picking.delivery_note), ('company_id', '=', picking.company_id.id), ('partner_id', '=', picking.partner_id.id), ('id', '!=', picking.id)]):
                    raise UserError(_("The delivery ticket has been duplicated. Please check!"))

    
    @api.multi
    def button_validate(self):
        self._check_duplicate_delivery_note()
        res = super(Picking, self).button_validate()
        return res
    
    
    @api.constrains('delivery_note')
    def _check_values(self):
        if self.delivery_note:
            if not self.delivery_note.isdigit():
                raise Warning(_('Delivery note should be numeric.'))
                return False
        return True
    
class StockMove(models.Model):
    _inherit = "stock.move"
    
    
    name = fields.Text(string = "Description")
    
    