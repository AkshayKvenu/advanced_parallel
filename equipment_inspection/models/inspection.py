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


class InspectionType(models.Model):
    _name = 'equipment.inspection.type'
    _description = 'Equipment Inspection Type'
    
    name = fields.Char('Type', required=True)
    code = fields.Char('Code', required=True) 
    sequence_id = fields.Many2one('ir.sequence')
    
    
    @api.model
    def create(self, vals):
        res = super(InspectionType, self).create(vals)
        seq = {
            'name':'Equipment Inspection',
            'implementation': 'no_gap',
            'code':'equipment.inspection',
            'prefix': res.code,
            'padding': 3,
            'number_increment': 1,
        }
        seq1 = self.env['ir.sequence'].sudo().create(seq)
        res.sequence_id = seq1
        
        return res


class Inspection(models.Model):
    _name = 'equipment.inspection'
    _description = 'Equipment Inspection'
    
    name = fields.Char()
    inspection_type_id = fields.Many2one('equipment.inspection.type', 'Type', required=True)
    date_inspect = fields.Date('Inspection Date', default=date.today())
    date_expiry = fields.Date('Expiry Date')
    equipment_id = fields.Many2one('maintenance.equipment', 'Equipment', required=True) 
    state = fields.Selection([('draft', 'Draft'), ('valid', 'Valid'), ('expire', 'Expired'), ('cancel', 'Cancelled')], default='draft')
    note = fields.Text('Notes')
    inspect_file = fields.Binary('Attachment', attachment=True)     
    
    
    @api.model
    def create(self, vals):
        if 'date_inspect' in vals and vals['date_inspect'] and 'date_expiry' in vals and vals['date_expiry']:
            if vals['date_inspect'] > vals['date_expiry']:
                raise UserError(_("Inspection Date should be less than Expiry Date"))
#             if vals['date_expiry'] :
            if type(vals['date_expiry']) == str:
                if vals['date_expiry'] <= str(date.today()):
                    raise UserError(_("Expiry Date should be grater than Today."))
            else:
                if vals['date_expiry'] <= date.today():
                    raise UserError(_("Expiry Date should be grater than Today."))
                
        name = ''
        inspection_type_obj = self.env['equipment.inspection.type'].browse(vals['inspection_type_id']).sequence_id
        name = inspection_type_obj.next_by_id()
        
        vals['name'] = name
        res = super(Inspection, self).create(vals)
        return res
    
    @api.multi
    def write(self, vals):
        date_inspect = 'date_inspect' in vals and vals['date_inspect'] or self.date_inspect
        date_expiry= 'date_expiry' in vals and vals['date_expiry'] or self.date_expiry
        if date_inspect and str(date_inspect) > str(date_expiry):
            raise UserError(_("Inspection Date should be less than Expiry Date"))
        if 'date_expiry' in vals and vals['date_expiry'] <= str(date.today()):
            raise UserError(_("Expiry Date should be grater than Today."))
        res = super(Inspection, self).write(vals)
        return res

    def action_set_valid(self):
        if not self.date_expiry:
            raise UserError(_("Please choose an Expiry Date to Validate."))
        if not self.inspect_file:
            raise UserError(_("Please choose an Attachment to Validate."))
        self.write({'state': 'valid'})
        
    def action_set_cancel(self):
        self.write({'state': 'cancel'})
    
        
    @api.multi
    @api.depends('name', 'date_expiry')
    def name_get(self):
        result = []
        for line in self:
            if line.date_expiry:
                name = line.name + ' [' + str(line.date_expiry) + ']'
            else:
                name = line.name
            result.append((line.id, name))
        return result
    
    @api.model
    def check_inspection_expiry(self):
        expire_inspection_ids = self.search([('date_expiry', '<', date.today()), ('state', '=', 'valid')])
        for inspection in expire_inspection_ids:
            inspection.write({'state': 'expire'})
    

        
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: