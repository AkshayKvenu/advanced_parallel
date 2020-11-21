# -*- coding: utf-8 -*-

import calendar

from odoo import models, fields, api, _
from _datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class AccrualAccounting(models.Model):
    _name = 'accrual.revenue.accounting'

    parent_id = fields.Many2one('accrual.revenue.accounting',default = False)
    company_id = fields.Many2one('res.company',default = lambda self: self.env.user.company_id)
    name = fields.Char("Name")
    original_value = fields.Float("Original Value")
    gross_increase_value = fields.Float("Gross Increase Value",default = 0)
    aquisition_date = fields.Date("Aquisition Date",default=date.today())
    residual_amnt_calculate = fields.Float("Residual Amount to calculate")
    residual_amount = fields.Float("Residual Amount to Recognize")
    deferred_amount = fields.Float("Deferred Revenue Amount")
    period = fields.Selection([('years', 'Years'), ('months', 'Months')],default = 'years')
    number_recognition = fields.Integer("Number Of Recognitions",default="5")
    posted_entries = fields.Integer("posted entries", compute='_posted_entry_count')
    gross_increase_count = fields.Integer("Gross Increase", compute='_posted_gross_increase_count')
    
    @api.multi
    def _posted_gross_increase_count(self):
        for asset in self:
            res = self.env['accrual.revenue.accounting'].search_count([('parent_id', '=', asset.id)])
            asset.gross_increase_count = res or 0
    
    @api.multi
    def _posted_entry_count(self):
        for asset in self:
            res = self.env['account.move'].search_count([('accrual_account_revenue_id', '=', asset.id), ('state', '=', 'posted')])
            asset.posted_entries = res or 0

#     delivery_count = fields.Integer("Posted Entries",default="5")
    first_recognition_date = fields.Date("First Recognition Date")
    deferred_amount_id = fields.Many2one('account.account',"Deferred Revenue Amount")
    expense_account_id = fields.Many2one('account.account',"Revenue Amount")
    move_id = fields.Many2one('account.move',"Move")
    depreciation_move_ids = fields.One2many('account.move','accrual_account_revenue_id', string="Revenue Board")
    original_move_line_ids = fields.One2many(comodel_name='account.move.line',inverse_name='move_line_revenue_id', string="Journal Items")

    journal_id = fields.Many2one('account.journal',"Journal")
    prorata_temporis = fields.Boolean('Prorata Temporis')
    prorata_date = fields.Date('Prorata Date',default=date.today())
    state = fields.Selection([('model', 'Model'), ('draft', 'Draft'), ('open', 'Running'), ('paused', 'On Hold'), ('close', 'closed')],
                              default='draft', string='Status')
                
    def compute_last_day(self,aquisition_date):  
       year = aquisition_date.strftime("%Y")
       month = aquisition_date.strftime("%m")
       day = calendar.monthrange(int(year), int(month))[1]
       last_date = date(int(year), int(month), int(day))
       return last_date        

        
    @api.onchange('original_value','gross_increase_value')
    def _compute_residual_values(self):
        self.residual_amnt_calculate = self.original_value
#         self.residual_amount = self.residual_amnt_calculate
#         self.deferred_amount = self.residual_amount + self.gross_increase_value

        
    @api.onchange('residual_amnt_calculate','gross_increase_value')
    def _compute_current_values(self):
        self.residual_amount = self.residual_amnt_calculate
        self.deferred_amount = self.residual_amount + self.gross_increase_value
    
    @api.model
    def create(self, vals):
        result = super(AccrualAccounting, self).create(vals)
        result.residual_amount = result.residual_amnt_calculate
        result.deferred_amount = result.residual_amount + result.gross_increase_value
        return result
                
    @api.multi
    def write(self, vals):
#         result = super(AccrualAccounting, self).write(vals)
        if 'residual_amnt_calculate' in vals:
            vals['residual_amount'] = vals['residual_amnt_calculate']
        if 'residual_amount' in vals:
            vals['deferred_amount'] = vals['residual_amount'] +self.gross_increase_value
            print("ddddddddddddddddddd",vals)
        if 'gross_increase_value' in vals:
            vals['deferred_amount'] = self.residual_amount + vals['gross_increase_value']
#             else :
#                 vals['deferred_amount'] = vals['residual_amount'] +self.gross_increase_value
        result = super(AccrualAccounting, self).write(vals)
        return result 
    
        
    @api.multi
    def gross_entries(self):
        asset_ids = []
        for asset in self.env['accrual.revenue.accounting'].search([('parent_id', '=', self.id)]):
            asset_ids.append(asset.id)
        return {
            'name': _('Gross Increase'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'accrual.revenue.accounting',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', asset_ids)],
                }
        
    @api.multi
    def open_entries(self):
        move_ids = []
        for asset in self:
            for depreciation_line in asset.depreciation_move_ids:
                if depreciation_line.id:
                    move_ids.append(depreciation_line.id)
        return {
            'name': _('Journal Entries'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', move_ids)],
                }

    @api.onchange('aquisition_date','period')
    def _compute_recognition_date(self):
        if self.aquisition_date and self.period:
            if self.period == "years":
                year = self.aquisition_date.strftime("%Y")
                self.first_recognition_date = date(int(year), 12, 31)
            else :
                self.first_recognition_date = self.compute_last_day(self.aquisition_date)
    
    @api.multi
    def action_cancel_accrual(self):
        return self.write({'state' : 'draft'})
    
    @api.multi
    def action_confirm_accrual(self):
        self.action_move_create()
        if self.depreciation_move_ids:
            for rec in self.depreciation_move_ids:
                rec.auto_post = True
        return self.write({'state' : 'open'})
    
    @api.multi
    def action_move_create(self):
        if not self.name:
            raise ValidationError(_("Field name is not defined"))
        if not self.deferred_amount_id:
            raise ValidationError(_("Field Deferred revenue amount is not defined"))
        if not self.expense_account_id:
            raise ValidationError(_("Field Revenue amount is not defined"))
        if not self.journal_id:
            raise ValidationError(_("Field Journal is not defined"))

        depreciation_move_list=[]
        self.env['account.move'].search([('accrual_account_revenue_id', '=',self.id)]).unlink()
        if self.residual_amount > 0:
            price_value = (self.residual_amount)/self.number_recognition
            number = 1
            rec_number = self.number_recognition
            if self.prorata_temporis and self.prorata_date:
                rec_number += 1
                number = 0
                if self.period == "months":
                    last_day = int(self.compute_last_day(self.prorata_date).strftime("%d"))
                    crnt_day= int(self.prorata_date.strftime("%d"))
                    percnt = (crnt_day-1)*100/last_day
                elif self.period == "years":
                    year = int(self.prorata_date.strftime("%Y"))
                    total_days =  int(date(year, 12, 31).strftime("%j"))
                    crnt_day = int(self.prorata_date.strftime("%j"))
                    percnt = (crnt_day)*100/total_days
                    
                last_price = round((price_value*percnt)/100,2)
                first_price = price_value - last_price
                
    #             setting dates for account move ```````````````
            date_list =[]    
            if self.period == "months":
                date_list = [self.compute_last_day(self.first_recognition_date + relativedelta(months=x)) for x in range(rec_number)]
            if self.period == "years":
                date_list = [self.first_recognition_date + relativedelta(years=x) for x in range(rec_number)]
    
            
            cumulative_value = 0.0
            for rec_date in date_list:
                iml = []
                name = self.name or ''
                name = name+"("+str(number)+"/"+str(self.number_recognition)+")"
                calculated_price = price_value
                if number == 0:
                    name = self.name+"(prorata entry)"
                    calculated_price = first_price
                elif number == self.number_recognition and self.prorata_temporis:
                    calculated_price = last_price
                number +=1
                if calculated_price >= 0.005:    
                    cumulative_value += calculated_price
                    iml.append({
                        'type': 'entry',
                        'name': self.name,
                        'price': calculated_price,
                        'account_id': self.deferred_amount_id.id,
                        'date_maturity': rec_date,
                        'amount_currency': False,
                        'debit': calculated_price,
                        'credit':0.0,
                        'currency_id': False,
                        'selfoice_id': self.id
                    })
                    iml.append({
                        'type': 'entry',
                        'name': self.name,
                        'price': calculated_price,
                        'account_id': self.expense_account_id.id,
                        'date_maturity': rec_date,
                        'amount_currency': False,
                        'debit': 0.0,
                        'credit':calculated_price,
                        'currency_id': False,
                        'selfoice_id': self.id
                    })
                    line = [(0, 0, l) for l in iml]
                    acc_move = {
                        'type': 'entry',
                        'ref': name,
                        'date': rec_date,
                        'amount_total' : calculated_price,
                        'asset_depreciated_value': cumulative_value,
                        'asset_remaining_value':self.residual_amount - cumulative_value,
                        'journal_id': self.journal_id.id,
                        'line_ids': line,
                        }
                    depreciation_move_list.append((0, False,acc_move))
            self.depreciation_move_ids = depreciation_move_list
        return True
    
# 
# class AccountMove(models.Model):
#     _inherit = 'account.move'  
#     
#     accrual_account_id = fields.Many2one('accrual.revenue.accounting',"Accrual account")
#     amount_total = fields.Float("Expense")
#     asset_depreciated_value = fields.Float("Cumulative Revenue")
#     asset_remaining_value = fields.Float("Next Period Expense")
#     auto_post = fields.Boolean('Post Automatically')
#     
#     def run_post_account_move(self):
#         for rec in self.search([]):
#             if rec.auto_post:
#                 if rec.date == date.today():
#                     self.action_post()
# 
#     @api.multi
#     def action_post(self):
#         record = super(AccountMove, self).action_post()
# #         print("ssssssssss",self.accrual_account_id.residual_amount)
#         if self.accrual_account_id:
#             residual = self.accrual_account_id.residual_amount - self.amount_total 
#             self.accrual_account_id.write({'residual_amnt_calculate': residual})
#         print("ssssssssss",self.accrual_account_id.residual_amount,residual,self.amount_total)
# #         print("ssssssssss",self.accrual_account_idq)
#         return record
#                 
    
  
  
  
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100