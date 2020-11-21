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

from odoo import models, fields, api

from datetime import datetime
import math

class HrContract(models.Model):
    _inherit = 'hr.contract'
    
    hra = fields.Float('HRA', digits=(16, 2))
    ta = fields.Float('TA', digits=(16, 2))
    other_allowance = fields.Float('Other Allowance', digits=(16, 2))
    food_allowance = fields.Float('Food Allowance', digits=(16, 2))
    gosi_local = fields.Float('GOSI LOCAL', digits=(16, 2))
    gosi_expat = fields.Float('GOSI EXPAT', digits=(16, 2))
    dependent_fee = fields.Float('Dependent fee', digits=(16, 2))
    gosi_employee = fields.Float('GOSI Employee', digits=(16, 2))
    total_package = fields.Float('Total Package', digits=(16, 2),readonly = True)
    
            
    @api.model
    def create(self, vals):
        result = super(HrContract, self).create(vals)
        if result.wage or result.hra or result.ta or result.food_allowance or result.other_allowance:
            result.total_package = result.wage + result.hra + result.ta + result.food_allowance + result.other_allowance
        return result
    
    @api.multi
    def write(self, vals):
        result = super(HrContract, self).write(vals)
        if self.wage or self.hra or self.ta or self.food_allowance or self.other_allowance:
            vals['total_package'] = self.wage + self.hra + self.ta + self.food_allowance + self.other_allowance
        result = super(HrContract, self).write(vals)
        return result
    
    @api.onchange('wage', 'hra', 'ta', 'food_allowance', 'other_allowance')
    def _onchange_total(self):
        if self.wage or self.hra or self.ta or self.food_allowance or self.other_allowance:
            self.total_package = self.wage + self.hra + self.ta + self.food_allowance + self.other_allowance
        
    

class EmployeeProfession(models.Model):
    _name = 'hr.employee.profession'
    
    name = fields.Char('Profession', required=True)
    arabic_name = fields.Char('Profession in Arabic', required=True)
    
    @api.multi
    def name_get(self):
        res = []
        for prof in self:
            name = prof.name + ' '+ prof.arabic_name
#             if analytic.code:
#                 name = _('[%(code)s] %(name)s') % {
#                     'code': analytic.code,
#                     'name': name,
#                 }
#             if analytic.partner_id:
#                 name = _('%(name)s - %(partner)s') % {
#                     'name': name,
#                     'partner': analytic.partner_id.commercial_partner_id.name,
#                 }
            res.append((prof.id, name))
        return res
     
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            args = ['|', ('name', operator, name), ('arabic_name', operator, name)] + args
        tags = self.search(args, limit=limit)
        return tags.name_get()
    
class HrEmployee(models.Model):
    _inherit = 'hr.employee'
     
    blood_group = fields.Selection([('A+','A+'), ('B+', 'B+'), ('AB+','AB+'), ('O+','O+'),
                                     ('A-','A-'), ('B-','B-'), ('AB-','AB-'), ('O-','O-')])
    gosi_no = fields.Char('GOSI ID')
    employee_profession_id = fields.Many2one('hr.employee.profession', 'Profession')
    certificate = fields.Selection(selection_add=[('diploma', 'Diploma'), ('elementary', 'Elementary School'), ('engineering', 'Engineering Degree Holder'), 
                                                  ('higher', 'Higher Secondary Passed'), ('middle', 'Middle School Passed'), ('secondary', 'Secondary Passed'), 
                                                  ('tech_edu', 'Technical Education Passed'), ('tech_inst', 'Technical Institute'), ('university', 'University Degree')])
        
class Salary_Rule(models.Model):
    _inherit = 'hr.payroll.structure'
    
    @api.model
    def default_get(self, fields):
        res = super(Salary_Rule, self).default_get(fields)
        res['parent_id'] = False
        return res
    
        
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
