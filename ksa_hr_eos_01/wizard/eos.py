# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _

class EosService(models.TransientModel):
    _name = "eos.service"
    _description = "End of service benefits"
    
    @api.model
    def _count(self):
        return len(self._context.get('active_ids', []))
    
    @api.model
    def _get_default_duration(self):
        if self._count() == 1:
            emp_eos_obj = self.env['employee.eos']
            emp_eos = emp_eos_obj.browse(self._context.get('active_ids'))[0]
            return emp_eos
    
    @api.model
    def _get_default_year_duration(self):
            return self._get_default_duration().duration_year
        
    @api.model
    def _get_default_month_duration(self):
        return self._get_default_duration().duration_month
    
    @api.model
    def _get_default_day_duration(self):
        return self._get_default_duration().duration_day

    @api.model
    def _get_default_date_from(self):
        return self._get_default_duration().joining_date

    @api.model
    def _get_default_date_end(self):
        return self._get_default_duration().relieving_date
    
#     @api.model
#     def _get_default_date_to(self):
#         return self._get_default_duration().date_end
    
    @api.model
    def _get_default_wage(self):
        return self._get_default_duration().wage
    
    limited_contract = fields.Selection([
        ('1', 'Expiration of the contract, or agreement of the parties to terminate the contract'),
        ('2', 'Termination of the contract by the employer'),
        ('3', 'Termination of the contract by the employer for a case in Article (80)'),
        ('4', 'Leaving the worker to work as a result of force majeure'),
        ('5', 'Termination of the labor contract to work within six months of the marriage contract, or within three months of the situation'),
        ('6', 'Worker to leave work for a case in Article (81)'),
        ('7', 'Termination of the contract by the worker or the worker to leave work for non-cases contained in Article (81)')
    ], string='Reason for End of Service')
    unlimited_contract = fields.Selection([
        ('1', 'Worker and the employer to terminate the contract agreement'),
        ('2', 'Termination of the contract by the employer'),
        ('3', 'Termination of the contract by the employer for a case in Article (80)'),
        ('4', 'Leaving the worker to work as a result of force majeure'),
        ('5', 'Termination of the labor contract to work within six months of the marriage contract, or within three months of the situation'),
        ('6', 'Worker to leave work for a case in Article (81)'),
        ('7', 'Leaving the worker to work without providing the resignation of cases is contained in Article (81) '),
        ('8', 'Resignation factor'),
    ], string='Reason for End of Service')
    contract_type = fields.Selection([
        ('fixed', 'Fixed term'),
        ('indefinite', 'Indefinite'),
    ], default="indefinite", string='Type of Contract',required=True)
    date_start = fields.Date('Start Date', default=_get_default_date_from)
    date_end = fields.Date('End Date', required=True, default=_get_default_date_end)
    wage = fields.Float('Wage', default=_get_default_wage)
    duration_year = fields.Integer('Duration', default=_get_default_year_duration)
    duration_month = fields.Integer('Duration in Months', default=_get_default_month_duration)
    duration_day = fields.Integer('Duration in Days', default=_get_default_day_duration)
    duration = fields.Char('Duration')

    @api.multi
    def button_confirm(self):
        employee_eos = self.env['employee.eos'].browse(self._context.get('active_ids', []))
        result = 0
        for record in employee_eos:
            salary = self.wage
            years = int(self.duration_year)+float(self.duration_month)/12+float(self.duration_day)/365
            if self.contract_type == 'fixed':
                if self.limited_contract == '3' or self.limited_contract == '7':
                    raise UserError(_('Not eligible end of service benefits'))
                else:
                    first = 0
                    second = 0
                    if (years > 5):
                        first = 5;
                        second = years - 5;
                    else:
                        first = years;
                    result = (first * salary * 0.5) + (second * salary)
            elif self.contract_type == 'indefinite':
                if self.unlimited_contract == '3':
                    raise UserError(_('Not eligible end of service benefits'))
                    break;
                if self.unlimited_contract == '7':
                    raise UserError(_('Not eligible end of service benefits'))
                    break;
                if self.unlimited_contract == '8':
                    if (years < 2):
                        raise UserError(_('Not eligible end of service benefits'))
                    elif (years <= 5):
                        result = (1 / 6) * salary * years;

                    elif (years <= 10):
                        result = ((1 / 3) * salary * 5) + ((2 / 3) * salary * (years - 5));
                    else:
                        result = (0.50 * salary * 5) + (salary * (years - 5));
                    break;
                if (years <= 5):
                    result = 0.5 * salary * years;
                else:
                    result = (0.5 * salary * 5) + (salary * (years - 5));
#             record.eos_amount = result
#             record.duration = self.duration
            record.update({
                'eos_amount': result,
                'duration': self.duration,
                'duration_day': self.duration_day,
                'duration_month': self.duration_month,
                'duration_year': self.duration_year,  
                'relieving_date': self.date_end,      
            })
        return {'type': 'ir.actions.act_window_close'}
    
    @api.onchange('date_start', 'date_end')
    def _onchange_date_start_end(self):
        if self.date_start and self.date_end:
            date_start = fields.Date.from_string(self.date_start)
            date_end = fields.Date.from_string(self.date_end)
            date_diff = relativedelta(date_end, date_start)
            self.duration_year = date_diff.years
            self.duration_month = date_diff.months
            self.duration_day = date_diff.days
            
            duration = ''
            if date_diff.years != 0:
                duration += str(date_diff.years) + ' Years '
            if date_diff.months != 0:
                duration += str(date_diff.months) + ' Months '
            if date_diff.days != 0:
                duration += str(date_diff.days) + ' Days '
            
            self.duration = duration
#             year = date_end.year - date_start.year - ((date_end.month, date_end.day) < (date_start.month, date_start.day))
#             self.duration_year = year       
#             month = date_end.month - date_start.month - ((date_end.month, date_end.day) < (date_start.month, date_start.day))
#             self.duration_month = month
#             day = date_end.day - date_start.day - ((date_end.month, date_end.day) < (date_start.month, date_start.day))
#             self.duration_day = day
#             
#             if year == 0:
#                 self.duration = str(month)+' Months'+str(day)+' Days'
#             elif month == 0:
#                 self.duration = str(year)+' Years'+str(day)+' Days'
#             elif day == 0:
#                 self.duration = str(year)+' Years'+str(month)+' Months'
#             else:
#                 self.duration = str(year)+' Years'+str(month)+' Months'+str(day)+' Days'
                
            

