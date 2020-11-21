# -- coding: utf-8 --

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
   
class ModifyData(models.TransientModel):
   _name = 'wizard.modify.expense'
        
   name = fields.Char("Reason")
   
   @api.model   
   def _get_object(self):
       accrual_id = self.env.context.get('active_id')
       return self.env['accrual.expense.accounting'].browse(accrual_id)
   
   @api.model   
   def _compute_residual(self):
       acc_obj = self._get_object()
       return acc_obj.residual_amount
   
   @api.model   
   def _compute_year(self):
       acc_obj = self._get_object()
       return acc_obj.period
   
   @api.model   
   def _compute_number(self):
       acc_obj = self._get_object()
       return acc_obj.number_recognition
   
   method_period = fields.Selection([('years', 'Years'), ('months', 'Months')], default=_compute_year)
   method_number = fields.Integer("Number Of Recognitions", default=_compute_number)
   gain_value = fields.Float("Gain value")
   need_date = fields.Boolean("Need date")
   date = fields.Date("Need date")
   account_asset_id = fields.Many2one('account.account',"Asset Gross Increase Account")
   account_asset_counterpart_id = fields.Many2one('account.account',"Account Asset Counterpart")
   account_depreciation_id = fields.Many2one('account.account',"Account Depreciation")
   account_depreciation_expense_id = fields.Many2one('account.account',"Account Depreciation Expense")
   value_residual = fields.Float("Depreciable Amount", default=_compute_residual)
   salvage_value = fields.Float("No Depreciable Amount")
   
   
   @api.onchange('value_residual')
   def _onchange_residual_values(self):
       acc_obj = self._get_object()
       self.gain_value = self.value_residual - acc_obj.residual_amount
       if self.gain_value > 0:
           self.date = acc_obj.aquisition_date
           self.need_date = True
           self.account_asset_id = acc_obj.deferred_amount_id
           self.account_depreciation_id = acc_obj.deferred_amount_id
           self.account_depreciation_expense_id = acc_obj.expense_account_id
   
   
   @api.multi
   def create_modify_expense(self):
       acc_obj = self._get_object()
       self.gain_value = self.value_residual - acc_obj.residual_amount
       print("Ssssssssssssssss",acc_obj.gross_increase_value)
       if self.gain_value > 0:
            acc_obj.gross_increase_value +=self.gain_value
            vals = {
                'name':acc_obj.name+":"+self.name,
                'parent_id':acc_obj.id,
                'original_value':self.gain_value,
                'residual_amnt_calculate':self.gain_value,
#                 'deferred_amount':self.gain_value,
                'aquisition_date':self.date,
                'period':self.method_period,
                'number_recognition':self.method_number,
                'deferred_amount_id':self.account_depreciation_id.id,
                'expense_account_id':self.account_depreciation_expense_id.id,
                'journal_id':acc_obj.journal_id.id,
                'state':'open'
                }
            accrual = self.env['accrual.expense.accounting'].create(vals)
            accrual._compute_recognition_date()
            
            accrual.action_move_create()
       

       accrual_id = self.env.context.get('active_id')
       return self.env['accrual.expense.accounting'].browse(accrual_id)
#    
# class RelatedPurchase(models.TransientModel): 
#     _name = 'wizard.related.purchase'
#    
#     move_line_ids = fields.Many2many('account.move.line', string="Move lines")
#    
#     
#     @api.multi
#     def action_get_move_lines(self):
#         accrual_model = self.env.context.get('active_model')
#         accrual_id = self.env.context.get('active_id')
#         accrual_obj = self.env[accrual_model].browse(accrual_id)
#         total = 0
#         if self.move_line_ids:
#             account_deffered = self.move_line_ids[0].account_id
#             for rec in self.move_line_ids:
#                 if accrual_model == 'accrual.expense.accounting':
#                     if rec.move_line_expense_id:
#                         raise ValidationError(_("This line is already used"))
#                 elif accrual_model == 'accrual.revenue.accounting':
#                     if rec.move_line_revenue_id:
#                         raise ValidationError(_("This line is already used")) 
#                     
#                 if account_deffered != rec.account_id:
#                     raise ValidationError(_("All the lines should be from the same account"))
#                     
#                 total += rec.credit
#             journal_obj = self.env['account.journal'].search([('type','=','general')], limit=1)
#     #         accrual_obj.residual_amount = total
#             accrual_obj.write({"original_value" :total ,
#                                'expense_account_id':account_deffered.id,
#                                'journal_id':journal_obj.id})
#             accrual_obj.original_move_line_ids = self.move_line_ids
#             