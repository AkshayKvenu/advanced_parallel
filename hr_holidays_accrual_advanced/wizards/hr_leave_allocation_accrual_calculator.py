# Copyright 2018-2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrLeaveAllocationAccrualCalculatorAccruement(models.TransientModel):
    _name = 'hr.leave.allocation.accrual.calculator.accruement'
    _description = 'HR Leave Allocation Accrual Calculator Accruement'

    calculator_id = fields.Many2one(
        string='Calculator',
        comodel_name='hr.leave.allocation.accrual.calculator',
    )
    days_accrued = fields.Float(
        string='Number of Days',
        readonly=True,
        required=True,
    )
    accrued_on = fields.Date(
        string='Accruement Date',
        readonly=True,
        required=True,
    )
    reason = fields.Char(
        string='Reason',
        readonly=True,
        required=True,
    )


class HrLeaveAllocationAccrualBalanceCalculator(models.TransientModel):
    _name = 'hr.leave.allocation.accrual.calculator'
    _description = 'HR Leave Allocation Accrual Calculator'

    date = fields.Date(
        string='Date',
        required=True,
    )
    accruement_ids = fields.One2many(
        string='Accruements',
        comodel_name=(
            'hr.leave.allocation.accrual.calculator.accruement'
        ),
        inverse_name='calculator_id',
        readonly=True,
    )
    accrued = fields.Float(
        string='Accrued',
        readonly=True,
    )
    balance = fields.Float(
        string='Balance',
        readonly=True,
    )

    @api.onchange(
        'date',
    )
    def _onchange(self):
        CalculatorAccruement = self.env[
            'hr.leave.allocation.accrual.calculator.accruement'
        ]
        accruement_ids = CalculatorAccruement

        if not self.date:
            self.update({
                'accrued': 0.0,
                'balance': 0.0,
                'accruement_ids': accruement_ids,
            })
            return
        
        leave_allocation = False
        
        if self.env.context.get('active_model') == 'hr.employee':
            allocation_obj = self.env['hr.leave.allocation'].search([('employee_id','=',self.env.context.get('active_id')),('state','=','validate'),('accrual','=','True')])
            for allocation in allocation_obj:
                if allocation_obj.holiday_status_id.is_annual_vacation:
                    leave_allocation = allocation
                    print("contxtttttttttttttttttttttttt",leave_allocation)
            
        else:    
            HrLeaveAllocation = self.env['hr.leave.allocation']
            leave_allocation = HrLeaveAllocation.browse(
                self.env.context.get('active_id')
            )
            print("contxtttttttttttttttttttttttt",leave_allocation)
            
        if not leave_allocation and self.date:
            raise UserError(_('No annual leave is allocated for you'))
            
        
        if leave_allocation:
                   
    
            accruements, accrued = leave_allocation._calculate_accrued_amount(
                datetime.combine(self.date, datetime.min.time()),
            )
    
            balance = 0.0
            for accruement in accruements:
                balance += accruement.days_accrued
                accruement_ids |= CalculatorAccruement.new({
                    'days_accrued': accruement.days_accrued,
                    'accrued_on': accruement.accrued_on,
                    'reason': accruement.reason,
                })
    
            self.update({
                'accrued': accrued,
                'balance': balance,
                'accruement_ids': accruement_ids,
            })
