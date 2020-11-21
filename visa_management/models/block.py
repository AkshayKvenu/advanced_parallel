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

class BlockVisa(models.Model):
    _name = 'hr.block.visa'
    _rec_name = 'visa_number'


    @api.model
    def _default_company(self):
        return self.env['res.company']._company_default_get('company.document.management')

    visa_number = fields.Char(string=' Block Visa No',required = True)
    date = fields.Date(string='Date')
    total_visa_no = fields.Integer(string=' Total Number of Visa',compute='count_employees')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', index=1,default=_default_company, readonly=True)
    remain_visa = fields.Integer(string=' Remaining Visa',compute='count_employees')
    add_inf = fields.Text('Additional Info', help='Additional Info', copy=False)
    block_visa_ids = fields.One2many('hr.employee.visa', 'visa_id', string="Visa")

  
    @api.depends('block_visa_ids')
    def count_employees(self):
        visa=[]
        emp =[]
        for rec in self.block_visa_ids:
            visa.append(rec)
            if rec.employee.id == False: 
                emp.append(rec)
        self.total_visa_no = len(visa)
        self.remain_visa = len(emp)
        
            
        
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
