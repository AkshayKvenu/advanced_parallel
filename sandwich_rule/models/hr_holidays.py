# -*- coding: utf-8 -*-
# © 2018-Today Aktiv Software (http://aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields,api,_
from odoo.exceptions import UserError, ValidationError
import datetime


class HrHolidays(models.Model):
    _inherit = "hr.leave"

    sandwich_rule = fields.Boolean('Sandwich Rule')
    hr_consider_sandwich_rule = fields.Boolean('Apply Sandwich Rule')

    @api.onchange('number_of_days_display','hr_consider_sandwich_rule')
    def check_leave_type(self):
        if self.hr_consider_sandwich_rule and self.employee_id and self.number_of_days_display:
            days=[]
            for each in self.employee_id.resource_calendar_id.attendance_ids:
                if int(each.dayofweek) not in days:
                    days.append(int(each.dayofweek))
            if self.date_from:
                leave_ids=self.env['hr.leave'].search([('employee_id','=',self.employee_id.id)])
                start_date=datetime.datetime.strptime(str(self.date_from).split(' ')[0], '%Y-%m-%d')
                number_date=start_date.weekday()
                date_list=[]
                if number_date == 0:
                    date_list.append(start_date - datetime.timedelta(days=1))
                    date_list.append(start_date - datetime.timedelta(days=2))
                    if max(days) == 4:
                        date_list.append(start_date - datetime.timedelta(days=3))
                if number_date == 4:
                    if max(days) == 4:
                        date_list.append(start_date + datetime.timedelta(days=1))
                        date_list.append(start_date + datetime.timedelta(days=2))
                        date_list.append(start_date + datetime.timedelta(days=3))
                if number_date == 5:
                    if max(days) == 5:
                        date_list.append(start_date + datetime.timedelta(days=1))
                        date_list.append(start_date + datetime.timedelta(days=2))
                for each in leave_ids:
                    if each.date_from:
                        if datetime.datetime.strptime(str(each.date_from).split(' ')[0], '%Y-%m-%d') in date_list:
                            self.sandwich_rule=True
            if self.number_of_days_display and self.date_from:
                start_date=str(self.date_from).split(' ')[0]
                end_date=str(self.date_to).split(' ')[0]
                number_of_leave=datetime.datetime.strptime(end_date, '%Y-%m-%d').date() - datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                cnt=0
                if number_of_leave:
                    rngs=0
                    if 'days' in str(number_of_leave):
                       rngs=int(str(number_of_leave).split(' days,')[0])
                    else:
                       rngs=int(str(number_of_leave).split(' day,')[0])
                    live_list=[]
                    for d_ord in range(rngs+1):
                        day = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=cnt)
                        cnt = cnt + 1
                        if max(days)==4:
                            if int(day.weekday()) == 5 or int(day.weekday()) == 6:
                                self.number_of_days_display = rngs
                        if max(days)==5:
                            if int(day.weekday()) == 6:
                                self.number_of_days_display = rngs
                        live_list.append(day.weekday())
                    if max(days)==4:
                        if 5 in live_list:
                            if 6 in live_list:
                                self.sandwich_rule=True
                            else:
                                self.sandwich_rule=False
                        else:
                                self.sandwich_rule=False
                    if max(days)==5:
                        if 6 in live_list:
                            self.sandwich_rule=True
                        else:
                            self.sandwich_rule=False
        else:
            if self.employee_id and self.date_from and self.date_to:
                self.sandwich_rule=False
                self.number_of_days_display = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)

    @api.onchange('date_from','date_to')
    def check_date_from_live(self):
        res = {}
        if self.employee_id:
            days=[]
            for each in self.employee_id.resource_calendar_id.attendance_ids:
                if int(each.dayofweek) not in days:
                    days.append(int(each.dayofweek))
            if self.date_from:
                start_date=datetime.datetime.strptime(str(self.date_from).split(' ')[0], '%Y-%m-%d')
                date_number=start_date.weekday()
                if date_number not in days:
                    res.update({'value': {'date_to': '','date_from': '','number_of_days_display':0.00,'sandwich_rule':False}, 'warning': {
                               'title': 'Validation!', 'message': 'This day is already holiday.'}})
            if self.date_to:
                end_date=datetime.datetime.strptime(str(self.date_to).split(' ')[0], '%Y-%m-%d')
                date_number=end_date.weekday()
                if date_number not in days:
                    res.update({'value': {'date_to': '','number_of_days_display':0.00,'sandwich_rule':False}, 'warning': {
                               'title': 'Validation!', 'message': 'This day is already holiday.'}})

        return res
    
    @api.onchange('holiday_status_id')
    def check_sandwich_rule(self):
        self.hr_consider_sandwich_rule = self.holiday_status_id.hr_consider_sandwich_rule_apply
        
class HolidaysType(models.Model):
    _inherit = "hr.leave.type"
    
    hr_consider_sandwich_rule_apply= fields.Boolean('Apply Sandwich Rule')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
