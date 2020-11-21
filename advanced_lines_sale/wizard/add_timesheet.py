# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2016 Amzsys IT Solutions Pvt Ltd
# (http://www.amzsys.com)
# info@amzsys.com
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
from openerp.osv import osv
from datetime import timedelta,date

class TimesheetWizard(models.TransientModel):
    _name = 'timesheet.wizard'
    _description = 'Add Timesheet Wizard'
    
    start_date = fields.Date(string="Start Date",required=True)
    end_date = fields.Date(string="End Date",required=True)


    @api.model
    def employee_assign(self):
        cru_user=self.env.user
        employee_id=self.env['hr.employee'].search([('user_id','=',cru_user.id)])
        if employee_id:
            return employee_id[0].id
        
    employee_id = fields.Many2one('hr.employee',string="Employee",required=True,default=employee_assign)
    

#     @api.onchange('start_date','end_date')
#     def date_validation(self):
#         if self.start_date and self.end_date and self.start_date > self.end_date:
#             raise osv.except_osv(('Error'), ('start date should be less than end date'))
#         context = self.env.context 
#         model=context.get('active_model')
#         task_ids=self.env[model].browse(context.get('active_ids'))
#         for task in task_ids:
#             print(self.end_date,date.today())
# #             if self.start_date and self.end_date:
#             if self.start_date and task.delivery_date and task.delivery_date > self.start_date:
#                 self.start_date = False
#                 raise osv.except_osv(('Error'), ('start date should be less than or equal to delivery date'))
#             if self.end_date and self.end_date <= date.today():
#                 self.end_date = False
#                 raise osv.except_osv(('Error'), ('end date should be less than or equal to today'))
            
    @api.multi
    def generate_template(self):
        start_date = self.start_date
        end_date = self.end_date
        context = self.env.context 
        model = context.get('active_model')
        task_ids = self.env[model].browse(context.get('active_ids'))
        if start_date > end_date:
            raise osv.except_osv(('Error'), ('start date should be less than end date'))
        for task in task_ids:
            if any(start_date <= rec.date <= end_date for rec in task.timesheet_ids):
                raise osv.except_osv(('Error'), ('Date already exist'))
            if start_date and task.delivery_date and task.delivery_date > start_date:
                raise osv.except_osv(('Error'), ('start date should be less than or equal to delivery date'))
            if end_date and end_date > date.today():
                raise osv.except_osv(('Error'), ('end date should be less than or equal to today'))
                  
            list = []
            while start_date <= end_date:
                list.append(start_date)
                start_date = start_date + timedelta(days = 1)
            
            for recs in list:
                vals = {'date': recs, 'employee_id': self.employee_id.id, 'name': 'Timesheet of ' + str(recs), 'unit_amount': 1.0, 'account_id': task.project_id.analytic_account_id.id, 'timesheet_invoice_id': False, 'task_id': task.id, 'project_id': task.project_id.id}
                self.env['account.analytic.line'].create(vals)
#                 task.timesheet_ids = [(0, 0, {'date': recs, 'employee_id': self.employee_id.id, 'name': 'Timesheet of ' + str(recs), 'unit_amount': 1.0, 'account_id': task.project_id.analytic_account_id.id, 'timesheet_invoice_id': False})]
  
  
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
         