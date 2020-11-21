# -- coding: utf-8 --

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
   
class RelatedPurchase(models.TransientModel): 
    _name = 'wizard.related.purchase'
   
   
    @api.model   
    def compute_type(self):
        accrual_model = self.env.context.get('active_model')
        print('aaaaaaaaaaaaaaaaaaaa!!!!!!!!!!!!!!!!!!!!!!!!!',self.env.context,accrual_model)
        if accrual_model == 'accrual.expense.accounting':
            return 'credit'
        elif accrual_model == 'accrual.revenue.accounting':
            return 'debit'
        
    account_type = fields.Char("type",default=compute_type)
    move_line_ids = fields.Many2many('account.move.line', string="Move lines")
   
    
    @api.multi
    def action_get_move_lines(self):
        accrual_model = self.env.context.get('active_model')
        accrual_id = self.env.context.get('active_id')
        accrual_obj = self.env[accrual_model].browse(accrual_id)
        total = 0
        account_field = ''
        if self.move_line_ids:
            account_id = self.move_line_ids[0].account_id
            for rec in self.move_line_ids:
                if accrual_model == 'accrual.expense.accounting':
                    account_field = 'deferred_amount_id'
                    total += rec.debit
                    if rec.move_line_expense_id:
                        raise ValidationError(_("This line is already used"))
                elif accrual_model == 'accrual.revenue.accounting':
                    account_field = 'expense_account_id'
                    total += rec.credit
                    if rec.move_line_revenue_id:
                        raise ValidationError(_("This line is already used")) 
                    
                if account_id != rec.account_id:
                    raise ValidationError(_("All the lines should be from the same account"))
                    
                
            journal_obj = self.env['account.journal'].search([('type','=','general')], limit=1)
    #         accrual_obj.residual_amount = total
            accrual_obj.write({"original_value" :total ,
                               account_field:account_id.id,
                               'residual_amnt_calculate':total,
                               'journal_id':journal_obj.id})
            accrual_obj.original_move_line_ids = self.move_line_ids
            