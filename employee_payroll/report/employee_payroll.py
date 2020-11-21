# -*- coding: utf-8 -*-

from odoo import api, models, _
from odoo.exceptions import UserError
# import pandas as pd   
import datetime  


class ReportPayroll(models.AbstractModel):
    _name = 'report.employee_payroll.report_payroll'

    @api.model
    def get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        total = []
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        
        payslips ={}
        
        codes = self.env['hr.salary.rule'].search([], order='sequence')
        
        code_list = [cc.code for cc in codes]   
        code_list = list(set(code_list))  
        
        payslips['code'] = code_list
        
        if docs.emp_ids:
            employee_ids = docs.emp_ids.ids
        else:
            employee_ids = self.env['hr.employee'].search([]).ids
            
        if docs.payroll_type == 'batch':
            pay_rec = docs.batch_id.slip_ids
        else:
            pay_rec = self.env['hr.payslip'].search([('date_from', '>=', docs.date_from), ('date_to', '<=', docs.date_to),  ('employee_id', 'in', employee_ids)])
        
        
        pay_list = {}
        for rec in pay_rec:
            pay_list.setdefault(datetime.datetime.strptime(str(rec.date_from), '%Y-%m-%d').date().strftime('%B-%Y'), []).append(rec)
        
        val_list = {}
        emp_list = {}
        for pay in pay_list:
            emp_list = dict((tp.employee_id, dict((code, 0) for code in code_list)) for tp in pay_list[pay])
            for slip in pay_list[pay]:
                for line in slip.line_ids:
                    emp_list[slip.employee_id][line.code] += line.total
            val_list[pay] = emp_list
        
        payslips['lines'] = val_list
        
        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': payslips,
        }


        

