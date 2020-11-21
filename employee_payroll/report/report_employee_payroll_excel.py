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

from odoo import models, api, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.employee_payroll.report_employee_payroll_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    @api.multi
    def get_lines(self, data=None):
        payslips ={}
        
        codes = self.env['hr.salary.rule'].search([('company_id', '=', data.company_id.id)], order='sequence')
        
        code_list = [cc.code for cc in codes] 
        code_list = list(dict.fromkeys(code_list))
        
        payslips['code'] = code_list
        
        if data.emp_ids:
            employee_ids = data.emp_ids.ids
        else:
            employee_ids = self.env['hr.employee'].sudo().search([('company_id', '=', data.company_id.id)]).ids
        
        if data.payroll_type == 'batch':
            pay_rec = data.batch_id.slip_ids.filtered(lambda slip: slip.employee_id.id in employee_ids)
        else:
            pay_rec = self.env['hr.payslip'].search([('date_from', '>=', data.date_from), ('date_to', '<=', data.date_to), ('employee_id', 'in', employee_ids)])
        
        pay_list = {}
        for rec in pay_rec:
            pay_list.setdefault(datetime.datetime.strptime(str(rec.date_from), '%Y-%m-%d').date().strftime('%B-%Y'), []).append(rec)
        
        val_list = {}
        emp_list = {}
        for pay in pay_list:
            emp_list = dict((tp.sudo().employee_id, dict((code, 0.00) for code in code_list)) for tp in pay_list[pay])
            for slip in pay_list[pay]:
                for line in slip.line_ids:
                    emp_list[slip.employee_id][line.code] += line.total
            val_list[pay] = emp_list
        
        payslips['lines'] = val_list
        return payslips
  
    def generate_xlsx_report(self, workbook, data, payroll):
        for obj in payroll:
            date_from = obj.date_from
            date_to = obj.date_to
            batch = obj.batch_id.name
            company = obj.company_id.name
            lines = self.get_lines(data = obj)
            code_len = len(lines['code'])
            
#             print ("lines ; ", lines)
            
            sheet = workbook.add_worksheet("Employee Payroll Statement")
            format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center', 'bold': True})
            format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
            format21 = workbook.add_format({'font_size': 10, 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
            format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 10})
            format31 = workbook.add_format({'bottom': True, 'top': True, 'align': 'center', 'font_size': 10})
             
            sheet.merge_range(2, 0, 2, code_len + 1, 'Employee Payroll Statement', format1)
            sheet.merge_range(3, 0, 3, code_len + 1, ' ')
            if obj.payroll_type == 'date':
                sheet.write(4, 0, 'From', format11)
                sheet.write(4, 1, str(date_from), format11)
                sheet.write(5, 0, 'To', format11)
                sheet.write(5, 1, str(date_to), format11)
            else:
                sheet.write(4, 0, 'Batch', format11)
                sheet.write(4, 1, batch, format11)
            
            sheet.write(4, 3, 'Company', format11)
            sheet.merge_range(4, 4, 4, 5, company, format11)
            sheet.merge_range(6, 0, 6, code_len + 1, ' ')
            
            w_row_no = 7
            
            sheet.write(7, 0, 'Employee Name', format11)
            sheet.write(7, 1, 'Employee ID', format11)
            sheet.write(7, 2, 'Job Position', format11)
            sheet.write(7, 3, 'Identification No', format11)
            sheet.write(7, 4, 'Bank Account No', format11)
            
            w_col_no = 5
            
            for code in lines['code']:
#                 print('aaaaaaaaaaaaaaaaaaa',code)
                sheet.write(w_row_no, w_col_no, code, format11)
                w_col_no += 1
            
            w_row_no += 1
            
            for month in lines['lines']:
                sheet.merge_range(w_row_no, 0, w_row_no, code_len + 1, month, format21)
                w_row_no += 1
                
                for emp in sorted(lines['lines'][month], key=lambda x: x.barcode):
                    sheet.write(w_row_no, 0, emp.name, format3)
                    sheet.write(w_row_no, 1, emp.barcode, format3)
                    sheet.write(w_row_no, 2, emp.job_id.name, format3)
                    sheet.write(w_row_no, 3, emp.identification_id, format3)
                    sheet.write(w_row_no, 4, emp.bank_account_id.acc_number, format3)
                    w_col_no = 5
                    for line in lines['lines'][month][emp]:
                        sheet.write(w_row_no, w_col_no, lines['lines'][month][emp][line], format3)
                        w_col_no += 1
                    
                    w_row_no += 1
                    
                sheet.merge_range(w_row_no, 0, w_row_no, 1, 'Total', format21)
                                    
                w_col_no = 5                    
                
                for code in lines['code']:
                    total = sum(lines['lines'][month][employee][code] for employee in lines['lines'][month])
                    sheet.write(w_row_no, w_col_no, total, format21)
                    w_col_no += 1
                w_row_no += 5
                    
                    
            
            


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
