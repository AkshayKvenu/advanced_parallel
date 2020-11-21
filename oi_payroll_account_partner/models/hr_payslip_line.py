'''
Created on Nov 4, 2018

@author: Zuhair Hammadi
'''
from odoo import models

class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'
    
    def _get_partner_id(self, credit_account):
        """
        Get partner_id of slip line to use in account_move_line
        """
        # use partner of salary rule or fallback on employee's address
        register_partner_id = self.salary_rule_id.register_id.partner_id.id
        if register_partner_id:
            return register_partner_id
        account = credit_account and self.salary_rule_id.account_credit or self.salary_rule_id.account_debit
        if account.reconcile:
            return self.slip_id.employee_id.address_home_id.id
        
        return False

