#-*- coding:utf-8 -*-

from odoo import models, fields, api

class Holidays(models.Model):
    _name = "hr.leave"
    _inherit = "hr.leave"
    
    def _default_approver(self):
        employee = self._default_employee()
        if employee.holidays_approvers:
                return employee.holidays_approvers[0].approver.id

    pending_approver = fields.Many2one('hr.employee', string="Pending Approver", readonly=True, default=_default_approver)
    pending_approver_user = fields.Many2one('res.users', string='Pending approver user', related='pending_approver.user_id', related_sudo=True, store=True, readonly=True)
    current_user_is_approver = fields.Boolean(string= 'Current user is approver', compute='_compute_current_user_is_approver')
    approbations = fields.One2many('hr.employee.holidays.approbation', 'holidays', string='Approvals', readonly=True)
    pending_transfered_approver_user = fields.Many2one('res.users', string='Pending transfered approver user', compute="_compute_pending_transfered_approver_user", search='_search_pending_transfered_approver_user')
    
    
    @api.multi
    def action_confirm(self):
        super(Holidays, self).action_confirm()
        for holiday in self:
            if holiday.employee_id.holidays_approvers:
                holiday.pending_approver = holiday.employee_id.holidays_approvers[0].approver.id
    
    @api.multi
    def action_approve(self):
        for holiday in self:
            is_last_approbation = False
            sequence = 0
            next_approver = None
            for approver in holiday.employee_id.holidays_approvers:
                sequence = sequence + 1
                if holiday.pending_approver.id == approver.approver.id:
                    if sequence == len(holiday.employee_id.holidays_approvers):
                        is_last_approbation = True
                    else:
                        next_approver = holiday.employee_id.holidays_approvers[sequence].approver
            if is_last_approbation:
                holiday.action_validate()
            else:
                holiday.write({'state': 'confirm', 'pending_approver': next_approver})
                self.env['hr.employee.holidays.approbation'].create({'holidays': holiday.id, 'approver': self.env.uid, 'sequence': sequence, 'date': fields.Datetime.now()})
            
    @api.multi
    def action_validate(self):
        self.write({'pending_approver': None})
        for holiday in self:
            self.env['hr.employee.holidays.approbation'].create({'holidays': holiday.id, 'approver': self.env.uid, 'date': fields.Datetime.now()})
        super(Holidays, self).action_validate()
    
    @api.one
    def _compute_current_user_is_approver(self):
        if self.pending_approver.user_id.id == self.env.user.id or self.pending_approver.transfer_holidays_approvals_to_user.id == self.env.user.id :
            self.current_user_is_approver = True
        else:
            self.current_user_is_approver = False
    
    @api.onchange('employee_id')
    def _onchange_employee(self):
        if self.employee_id and self.employee_id.holidays_approvers:
            self.pending_approver = self.employee_id.holidays_approvers[0].approver.id
        else:
            self.pending_approver = False
            
    @api.one
    def _compute_pending_transfered_approver_user(self):
        self.pending_transfered_approver_user = self.pending_approver.transfer_holidays_approvals_to_user
    
    def _search_pending_transfered_approver_user(self, operator, value):
        replaced_employees = self.env['hr.employee'].search([('transfer_holidays_approvals_to_user', operator, value)])
        employees_ids = []
        for employee in replaced_employees:
            employees_ids.append(employee.id)
        return [('pending_approver', 'in', employees_ids)]
    