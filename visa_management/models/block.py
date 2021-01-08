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

from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError, ValidationError
from lxml import etree
from odoo.osv.orm import setup_modifiers

class BlockVisa(models.Model):
    _name = 'hr.block.visa'
    _rec_name = 'visa_number'


    @api.model
    def _default_company(self):
        return self.env['res.company']._company_default_get('company.document.management')
    

    visa_number = fields.Char(string=' Block Visa No',required = True)
    
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm')], default='draft', string='draft')
    
    sponser_number = fields.Char(string='Sponser Number')
    date = fields.Date(string='Date')
    expiry_date = fields.Date(string='Expiry Date')
    total_visa_no = fields.Integer(string=' Total Number of Visa',compute='count_employees')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', index=1,default=_default_company, readonly=True)
    remain_visa = fields.Integer(string=' Remaining Visa',compute='count_employees')
    add_inf = fields.Text('Additional Info', help='Additional Info', copy=False)
    block_visa_ids = fields.One2many('hr.employee.visa', 'visa_id', string="Visa")
    profession_ids = fields.One2many('hr.visa.profession', 'block_visa_id', string="Profession")

#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(BlockVisa, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
#         if 'params' in self.env.context:
#             print("cccccccccccccccc",self.env.context)
#             block_id = self.env.context['params']['id']
#             active_model = self.env.context['params']['model']
#             print("BBbbbbbbbbbbbbbbbbb",active_model, block_id)
#             print("eeeeeeeeeeeeeeeeeeee",self.env.context, self.state)
#     #         if active_model == 'hr.block.visa' and block_id:
#             block_obj = self.env['hr.block.visa'].browse(block_id)
#             doc = etree.XML(result['arch'])
#             if block_obj.state == 'confirm' and doc.xpath("//field[@name='block_visa_ids']/field[@name='allocate']"):
#                 print("Aaaaaaaaaaaaaa")
#                 node = doc.xpath("//field[@name='block_visa_ids']/field[@name='allocate']")[0]
#                 node.set('invisible', '1')
#                 setup_modifiers(node, result['fields']['method_number'])
#             result['arch'] = etree.tostring(doc, encoding='unicode')
#         return result
        
  
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
        
    def action_confirm(self):
        if self.state == 'draft':
            for line in self.profession_ids:
                for i in range(line.quantity):
                    name = self.visa_number +'-'+ line.country.name+str(i)
                    self.env['hr.employee.visa'].create({'visa_num':name, 'profession':line.category, 'visa_id':self.id})
            self.write({'state':'confirm'})
        
    def action_draft(self):
        if self.state == 'confirm':
            for lines in self.block_visa_ids:
                lines.unlink()
            self.write({'state':'draft'})
            
            
        
    def compute_visa(self):
        for line in self.profession_ids:
            name = self.visa_number +'-'+ line.country.name
            self.env['hr.employee.visa'].create({'visa_num':name, 'profession':line.category, 'visa_id':self.id})

class ProfessionVisa(models.Model):
    _name = 'hr.visa.profession'
        
    parent_state = fields.Selection(related='block_visa_id.state', string='Parent State')
    category = fields.Char(string='Category')
    country = fields.Many2one('res.country', string='Country')
    quantity = fields.Integer(string='Qty')
    allocate = fields.Integer(string='Allocate')
    stamped = fields.Integer(string='Stamped')
    deployed = fields.Integer(string='Deployed', compute='_compute_deployed')
    balance = fields.Integer(string='Balance', compute='_compute_balance')
    note = fields.Char(string='Comments')
    block_visa_id = fields.Many2one('hr.block.visa', string='Category visa')
    
    def _compute_deployed(self):
        for rec in self:
            deployed = 0
            for lines in rec.block_visa_id.block_visa_ids:
                if lines.employee and lines.profession == rec.category:
                    deployed +=1
            rec.deployed = deployed
    
    @api.depends('quantity','allocate','stamped','deployed')
    def _compute_balance(self):
        for rec in self:
            rec.balance = rec.quantity - (rec.allocate + rec.stamped + rec.deployed)

    @api.constrains('quantity')
    def quantity_validation(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_('Quantity should not be less than or equal to zero.'))
            
        
    @api.multi
    def unlink(self):
        for line in self:
            if line.parent_state == 'confirm':
                raise UserError(_('Cannot delete a visa lines which is in Confirm state.'))
        return super(ProfessionVisa, self).unlink()
    
    @api.model
    def create(self, values):
        res = super(ProfessionVisa, self).create(values)
        if res.parent_state == 'confirm':
            raise UserError(_('Cannot create a visa lines which is in Confirm state.'))
        return res

        
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
