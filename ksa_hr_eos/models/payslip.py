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
from odoo.exceptions import UserError, ValidationError, Warning
from odoo import models, fields, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    eos_id = fields.Many2one('employee.eos', string="End Of Service", readonly=True)
    
    
    @api.model
    def create(self, vals):
        res = super(HrPayslip, self).create(vals)
        employee_eos = self.env['employee.eos'].search([('employee_id', '=', res.employee_id.id), ('state', '=', 'done')], limit=1)
        if employee_eos and res.date_from <= employee_eos.effective_date <= res.date_to:
            res.update({'eos_id': employee_eos.id,})
        return res
    
    @api.multi
    def write(self, vals):
        employee_id = vals['employee_id'] if 'employee_id' in vals and vals['employee_id'] else self.employee_id.id
        date_from = vals['date_from'] if 'date_from' in vals and vals['date_from'] else self.date_from
        date_to = vals['date_to'] if 'date_to' in vals and vals['date_to'] else self.date_to
        employee_eos = self.env['employee.eos'].search([('employee_id', '=', employee_id), ('state', '=', 'done')], limit=1)
        if employee_eos and date_from <= employee_eos.effective_date <= date_to:
            vals.update({'eos_id': employee_eos.id,})
        res = super(HrPayslip, self).write(vals)
        return res
    
    
    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        res = super(HrPayslip, self).onchange_employee()
        employee_eos = self.env['employee.eos'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'done')], limit=1)
        if employee_eos and self.date_from <= employee_eos.effective_date <= self.date_to:
            days = fields.Date.from_string(employee_eos.relieving_date).day
            name = 'End of service from '+ str(employee_eos.joining_date)+ ' to ' + str(employee_eos.relieving_date)
            self.update({'input_line_ids': [(0, 0, {'name': name, 'code': 'eos', 'amount': employee_eos.eos_amount, 'contract_id': self.contract_id}),
                                            (0, 0, {'name': 'Leave Encashment', 'code': 'lsal', 'amount': employee_eos.eos_leave_salary, 'contract_id': self.contract_id})],
                        'worked_days_line_ids': [(0, 0, {'name': name, 'code': 'eos', 'number_of_days': days, 'contract_id': self.contract_id})],
                        'eos_id': employee_eos.id,
                    })
        else:
            self.update({'eos_id': False,})
                     
        return res
    
class Contract(models.Model):
    _inherit = "hr.contract"
    
    gosi_wage = fields.Float('GOSI Wage', digits=(16, 2), help="GOSI wage of the employee")
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
