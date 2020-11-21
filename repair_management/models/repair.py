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

class RepairManagement(models.Model):
    _inherit='repair.order'
    
    analytic_account_id = fields.Many2one('account.analytic.account',string = 'Analytic Account')
    date = fields.Date(string='Date')
    
    @api.multi
    def action_repair_done(self):
        res = super(RepairManagement, self).action_repair_done()
        for rec in self:
            for move in rec.operations.move_id.account_move_ids:
                for line in move.line_ids:
                    line.analytic_account_id = rec.analytic_account_id
                if rec.date:
                    move.date = rec.date                
        return res
        
    
class RepairLine(models.Model):
    _inherit='repair.line'
    
            
    @api.onchange('product_uom')
    def _onchange_product_uom(self):
        res = super(RepairLine, self)._onchange_product_uom()
        if self.type == 'add':
            self.price_unit = self.product_id.standard_price
        return res

class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self):
        res = super(StockMove, self)._action_done()
        print("rrrrrrrrrrrrrrrrrr",res)
        
        
        
        
        
        
        



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
