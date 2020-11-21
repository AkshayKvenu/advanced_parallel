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

from odoo import models, fields, api, _

class EmployeePayrollReport(models.TransientModel):
    _inherit = "account.common.partner.report"
    _name = 'emp.pay.report'
     
    emp_ids = fields.Many2many('hr.employee', string="Employees", domain="[('company_id', '=', company_id)]")
    payroll_type = fields.Selection([('date', 'Date'), ('batch', 'Batch')], default='date', string='Payroll by')
    batch_id = fields.Many2one('hr.payslip.run', 'Batch')
    
    
    @api.onchange('batch_id')
    def _get_batch_company(self):
        if self.batch_id:
            self.company_id = self.batch_id.journal_id.sudo().company_id.id
        
    
    def _print_report(self, data):
        data = self.pre_print_report(data)
        return self.env.ref('employee_payroll.action_report_employee_payroll').report_action(self, data=data)
      
    @api.multi
    def pre_print_report(self, data):
        data = super(EmployeePayrollReport, self).pre_print_report(data)
        data['form'].update(self.read(['emp_ids'])[0])
        data['form'].update(self.read(['payroll_type'])[0])
        data['form'].update(self.read(['batch_id'])[0])
        return data
    
    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
                return self.env.ref('employee_payroll.report_employee_payroll_xlsx').report_action(self, data=datas)
    

    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
