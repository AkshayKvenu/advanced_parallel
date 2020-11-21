# -*- coding: utf-8 -*-

import calendar

from odoo import models, fields, api, _
from _datetime import date, timedelta



class AccountMove(models.Model):
    _inherit = 'account.move'  
    
    accrual_account_expense_id = fields.Many2one('accrual.expense.accounting',"Accrual account")
    accrual_account_revenue_id = fields.Many2one('accrual.revenue.accounting',"Accrual account")
    amount_total = fields.Float("Expense")
    asset_depreciated_value = fields.Float("Cumulative Expense")
    asset_remaining_value = fields.Float("Next Period Expense")
    auto_post = fields.Boolean('Post Automatically')
    
    def run_post_account_move(self):
        for rec in self.search([]):
            if rec.auto_post:
                if rec.date == date.today():
                    self.action_post()

    @api.multi
    def action_post(self):
        record = super(AccountMove, self).action_post()
        if self.accrual_account_expense_id:
            residual = self.accrual_account_expense_id.residual_amount - self.amount_total 
            self.accrual_account_expense_id.write({'residual_amnt_calculate': residual})
        elif self.accrual_account_revenue_id:
            residual = self.accrual_account_revenue_id.residual_amount - self.amount_total 
            self.accrual_account_revenue_id.write({'residual_amnt_calculate': residual})
            
        return record

    
class AccountMoveLines(models.Model):
    _inherit = 'account.move.line'  
       
    move_line_expense_id = fields.Many2one('accrual.expense.accounting','Accrual move line')
    move_line_revenue_id = fields.Many2one('accrual.revenue.accounting','Accrual revenue move line')
#     move_line_wizard_id = fields.Many2one('wizard.related.purchase','move line')
                   