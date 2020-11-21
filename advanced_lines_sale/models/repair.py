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
from odoo import models, fields, api

class Repairvendor(models.Model):
    _inherit = 'repair.fee'
    
    repair_vendor_id= fields.Many2one('res.partner', 'Vendor')
    
    
class RepairOrder(models.Model):
    _inherit = 'repair.order'
    
    @api.multi
    def action_repair_start(self):
        res = super(RepairOrder, self).action_repair_start()
        self.lot_id.write({'state': 'maintenance'})
        task_ids = self.sudo().env['project.task'].search([('lot_id', '=', self.lot_id.id),('state', '=' ,'rent')], limit=1)
        if task_ids:
            task_ids.state = 'maintenance'
        return res
    
    def _revert_lot_state(self):
        task_ids = self.sudo().env['project.task'].search([('lot_id', '=', self.lot_id.id), ('state', '=' ,'maintenance')], limit=1)
        if task_ids:
            task_ids.state = 'rent'
            self.lot_id.write({'state': 'rent'})
        else:
            self.lot_id.write({'state': 'ready'}) 

    @api.multi
    def action_repair_end(self):
        res =  super(RepairOrder, self).action_repair_end()
        self._revert_lot_state()            
        return res

    @api.multi
    def action_repair_cancel(self):
        if self.filtered(lambda repair: repair.state == 'done'):
            raise UserError(_("Cannot cancel completed repairs."))
        if any(repair.invoiced for repair in self):
            raise UserError(_('The repair order is already invoiced.'))
        self.mapped('operations').write({'state': 'cancel'})
        if self.state == 'under_repair':
            self._revert_lot_state()
        return self.write({'state': 'cancel'})
        




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: