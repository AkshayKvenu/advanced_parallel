# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 Amzsys IT Solutions Pvt Ltd
#    (http://www.amzsys.com)
#    info@amzsys.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models
import datetime
from odoo.exceptions import UserError, ValidationError


class EmployeeVisa(models.Model):
    _name = 'hr.employee.visa'
    _rec_name = 'name'


    name = fields.Char('Name', compute='compute_name')
    
    visa_num = fields.Char(string='Visa No',required=True)
    profession = fields.Char(string='Profession',required=True) 
    employee = fields.Many2one('hr.employee', string="Employee", readonly=True)
    visa_id = fields.Many2one('hr.block.visa', string="Block Visa", readonly=True)
    
    @api.depends('visa_num','profession')
    def compute_name(self):
        for rec in self:
            rec.name = rec.visa_num +"["+ rec.profession+"]"

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    visa_numb = fields.Many2one('hr.employee.visa', string="Visa No")
    prof = fields.Char(string='Profession', related='visa_numb.profession', readonly=True)
    

    @api.model
    def create(self, vals):
        if 'visa_numb' in vals and vals['visa_numb']:
            object = self.env['hr.employee.visa'].browse(vals['visa_numb'])
            vals['prof'] = object.profession
#             result.prof = result.visa_numb.profession
        result = super(HrEmployee, self).create(vals)
        if result.visa_numb:
            result.visa_numb.employee = result.id
    
        return result

    
    @api.multi
    def write(self, vals):
        if self.visa_numb:
            self.visa_numb.employee = False
        if 'visa_numb' in vals and vals['visa_numb']:
            object = self.env['hr.employee.visa'].browse(vals['visa_numb'])
            vals['prof'] = object.profession
            object.employee = self.id
        else:
            vals['prof'] = False
        result = super(HrEmployee, self).write(vals)
        return result

    
    @api.onchange('visa_numb')
    def onchange_visa_numb(self):
        if self.visa_numb:
            self.prof = self.visa_numb.profession
#             self.visa_numb.employee = self.id
        else:
            self.prof = False
         

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
