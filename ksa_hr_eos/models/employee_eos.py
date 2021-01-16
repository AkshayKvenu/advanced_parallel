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

import datetime
from datetime import datetime
from dateutil import relativedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError, Warning
from odoo import models, fields, api, _
from math import fabs

class EmployeeEOS(models.Model):
    _name = "employee.eos"
    _rec_name = 'employee_id'
    
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    department_id = fields.Many2one('hr.department', string='Department',readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Title',readonly=True)
    country_id = fields.Many2one('res.country', string='Nationality (Country)')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status')
    birthday = fields.Date('Date of Birth')
    identification_id = fields.Char(string='Identification No')
    work_location = fields.Char('Work Location',readonly=True)
    parent_id = fields.Many2one('hr.employee', string='Manager',readonly=True)
    contract_ids = fields.One2many(related='employee_id.contract_ids', string="Contracts")
    contract_id = fields.Many2one('hr.contract', related='employee_id.contract_id', string='Current Contract')
    date_start = fields.Date('Start Date', related='contract_id.date_start')
    date_end = fields.Date('End Date', related='contract_id.date_end')
    age = fields.Char('Age')
    duration = fields.Char('Duration')
    wage = fields.Monetary('Wage')
    eos_amount = fields.Float('End Services Benefits',readonly=True)
    duration_year = fields.Integer('Duration in Years')
    duration_month = fields.Integer('Duration in Months')
    duration_day = fields.Integer('Duration in Days')
    currency_id = fields.Float(string="Currency")
    effective_date = fields.Date('Effective Date', help="The date at which this amount shows in Payroll.")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft')
    joining_date = fields.Date('Joining Date')
    relieving_date = fields.Date('Relieving Date')
    note = fields.Text('Additional Information', readonly=True, states={'draft': [('readonly', False)]})
    balance = fields.Float(string='Balance', readonly=True)
    eos_leave_salary = fields.Float('EOS Leave Salary',readonly=True)
    show_leave_salary = fields.Boolean('Show Leave Salary')
    
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id
            self.department_id = self.employee_id.department_id
            self.country_id = self.employee_id.country_id
            self.gender = self.employee_id.gender
            self.marital = self.employee_id.marital
            self.birthday = self.employee_id.birthday
            self.identification_id = self.employee_id.identification_id
            self.work_location = self.employee_id.work_location
            self.parent_id = self.employee_id.parent_id
            self.joining_date = self.employee_id.joining_date
            self.wage = self.contract_id.total_package
    
    @api.onchange('birthday')
    def _onchange_birthday(self):
        if self.birthday:
            today = datetime.datetime.utcnow().date()
            born = fields.Date.from_string(self.birthday)
            self.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            
    @api.onchange('date_start','date_end')
    def _onchange_date_start_end(self):
        if self.date_start and self.date_end:
            date_start = fields.Date.from_string(self.date_start)
            date_end = fields.Date.from_string(self.date_end)
            year = date_end.year - date_start.year - ((date_end.month, date_end.day) < (date_start.month, date_start.day))
            self.duration_year = year
            month = date_end.month - date_start.month - ((date_end.month, date_end.day) < (date_start.month, date_start.day))
            self.duration_month = month
            day = date_end.day - date_start.day - ((date_end.month, date_end.day) < (date_start.month, date_start.day))
            self.duration_day = day
            self.duration = str(year)+' Years'+str(month)+' Months'+str(day)+' Days'
            
            
    def action_done(self):
        if not self.effective_date:
            raise Warning(_("Please give 'Effective Date' to Confirm."))
        employee = self.env['employee.eos'].search([('employee_id','=', self.employee_id.id),('state','=','done')])
        if employee:
            raise Warning(_("'End of Service' already exist for %s.") % self.employee_id.name)
        return self.write({'state' : 'done'})
    
    def action_cancel(self):
        employee_payslip = self.env['hr.payslip'].search([('eos_id', '=', self.id)])
        if employee_payslip:
            raise UserError(_("You cannot cancel an 'EOS' which is used in Payslip."))
        return self.write({'state' : 'cancel'})
    
    def acton_reset_draft(self):
        return self.write({'state' : 'draft'})
    
    @api.model
    def create(self, vals):
        result = super(EmployeeEOS, self).create(vals)
        if result.employee_id.department_id or result.employee_id.job_id or result.employee_id.work_location or result.employee_id.parent_id :
            result.department_id = result.employee_id.department_id
            result.job_id = result.employee_id.job_id
            result.work_location = result.employee_id.work_location
            result.parent_id = result.employee_id.parent_id
            result.wage = result.contract_id.total_package
        return result
    
    @api.multi
    def write(self, vals):
        employee_id = 'employee_id' in vals and vals['employee_id'] or self.employee_id.id
        employee = self.env['hr.employee'].browse(employee_id)
        vals.update({
            'department_id': employee.department_id.id,
            'job_id': employee.job_id.id,
            'work_location': employee.work_location,
            'parent_id': employee.parent_id.id,
            'wage': employee.contract_id.total_package,
        })
        result = super(EmployeeEOS, self).write(vals)
        return result
    
    
    @api.multi
    def calculate_leave_salary(self):
        for vals in self:
            if vals.relieving_date:
                relieving_date_new = vals.relieving_date + relativedelta(months=+1)
                no_of_days = relieving_date_new - vals.relieving_date
                vals.eos_leave_salary = (vals.wage/no_of_days.days)*vals.balance
            
            
#     @api.multi
#     def calculate_eos(self):
#         self.eos_amount = self.duration_year > 5 and (self.wage * (self.duration_year - 5) + self.wage * .5 * 5) or ( self.wage * .5 * self.duration_year )




