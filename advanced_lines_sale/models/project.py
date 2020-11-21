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
from odoo.exceptions import ValidationError,Warning

from datetime import date

class Project(models.Model):
    _inherit = 'project.project'

    @api.constrains('sale_line_id', 'billable_type')
    def _check_sale_line_type(self):
        for project in self:
            if project.billable_type == 'task_rate':
                if project.sale_line_id and project.sale_line_id.product_id.is_rental:
                    return True
                if project.sale_line_id and not project.sale_line_id.is_service:
                    raise ValidationError(_("A billable project should be linked to a Sales Order Item having a Service product."))
                if project.sale_line_id and project.sale_line_id.is_expense:
                    raise ValidationError(_("A billable project should be linked to a Sales Order Item that does not come from an expense or a vendor bill."))

class Task(models.Model):                    
    _inherit = 'project.task'
    
    product_id = fields.Many2one('product.product', 'Product')
    lot_id = fields.Many2one('stock.production.lot', 'Lot')
    delivery_date = fields.Date(string='Delivery Date')
    state = fields.Selection([('rent', 'On Rent'), ('maintenance', 'Under Maintenance'), ('demobilize', 'Demobilized')], string='Status')
    return_stock_picking_id = fields.Many2one('stock.picking', 'Return Picking')
    stock_move_line_id = fields.Many2one('stock.move.line', 'Move Line')
    
    @api.model
    def create(self, vals):
        vals['delivery_date']=date.today()
        lines = super(Task, self).create(vals)
        return lines
    
    @api.multi
    @api.constrains('sale_line_id')
    def _check_sale_line_type(self):
        for task in self.sudo():
            if task.sale_line_id:
                if task.sale_line_id.sale_type == 'rent':
                    return True
                if not task.sale_line_id.is_service or task.sale_line_id.is_expense:
                    raise ValidationError(_('You cannot link the order item %s - %s to this task because it is a re-invoiced expense.' % (task.sale_line_id.order_id.id, task.sale_line_id.product_id.name)))

    @api.multi
    def action_set_maintenance(self):
        self.lot_id.write({'state': 'maintenance'})
        self.write({'state': 'maintenance'})
        
    @api.multi
    def action_set_rent(self):
        self.lot_id.write({'state': 'rent'})
        self.write({'state': 'rent'})
        
    @api.multi
    def action_set_demobilize(self):
        return_obj = self.env['stock.return.picking']
        context = {'active_id': self.stock_move_line_id.picking_id.id}
        return_id = return_obj.with_context(context).create({'picking_id': self.stock_move_line_id.picking_id.id, 
                                       'product_return_moves': [(0, 0, {'product_id': self.product_id.id, 'quantity': 1.0, 'move_id': self.stock_move_line_id.move_id.id, 'uom_id': self.product_id.uom_id.id})]})
        return_picking = return_id.create_returns()
        return_picking_id = self.env['stock.picking'].browse(return_picking['res_id'])
        
        if return_picking_id.move_ids_without_package.move_line_ids:
            return_picking_id.move_ids_without_package.move_line_ids[0].update({'lot_id': self.lot_id.id, 'qty_done': 1.0})
        
        self.write({
            'return_stock_picking_id': return_picking['res_id'],
            'state': 'demobilize'
        })
        
        return return_picking
    
    @api.multi
    def write(self, vals):
        if self.state == 'demobilize':
            raise Warning("You cannot update the record")
        return super(Task, self).write(vals)
     
    
        
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: