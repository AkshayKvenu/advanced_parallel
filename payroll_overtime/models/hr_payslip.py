
import datetime

from odoo import models, fields, api,_
from odoo.exceptions import UserError
    
class Hr_Payslip(models.Model):
    
    _inherit = 'hr.payslip'   
        
    @api.constrains('employee_id', 'contract_id', 'date_from', 'date_to')
    def lines_create(self):
        parent_account = self.env['hr.payroll_overtime.lines'].search([('employee_id', '=', self.employee_id.id),('state', '=', 'done')])
        for rec in self.worked_days_line_ids:
            if rec.code == 'ot':
                rec.unlink()
        if parent_account and self.contract_id:
            ot=0
            for rec in parent_account:
                if rec.start_date >= self.date_from and rec.end_date <= self.date_to:
                    ot += rec.OT_float
            if ot > 0:
                ot_line = {'name' : 'Overtime', 'payslip_id' : self.id, 'sequence' : 7, 'code' : 'ot', 'number_of_days': 0.0, 'number_of_hours' : ot, 'contract_id' : self.contract_id.id}
                self.worked_days_line_ids = [(0, 0, ot_line)]
        
  