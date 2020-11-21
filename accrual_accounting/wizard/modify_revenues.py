# -- coding: utf-8 --

from odoo import models, fields, api, _

   
class ModifyData(models.TransientModel):
   _name = 'wizard.modify.revenues'
        
   name = fields.Char("Reason")
   
   @api.model   
   def _get_object(self):
       accrual_id = self.env.context.get('active_id')
       return self.env['accrual.revenue.accounting'].browse(accrual_id)
   
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
            accrual = self.env['accrual.revenue.accounting'].create(vals)
            accrual._compute_recognition_date()
            
            accrual.action_move_create()
       
