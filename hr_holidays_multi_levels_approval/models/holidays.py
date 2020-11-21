#-*- coding:utf-8 -*-

from odoo import models, fields, api

class Holidays(models.Model):
    _name = "hr.leave"
    _inherit = "hr.leave"
    
    
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
        ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
        help="The status is set to 'To Submit', when a leave request is created." +
        "\nThe status is 'To Approve', when leave request is confirmed by user." +
        "\nThe status is 'Refused', when leave request is refused by manager." +
        "\nThe status is 'Approved', when leave request is approved by manager.")
    
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
                
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
                email_to = holiday.pending_approver.work_email  
                template = self.env.ref('hr_holidays_multi_levels_approval.hr_leave_approve_request_email_template', False)
                template_id = self.env['mail.template'].browse(template.id)
                template_id.with_context(url=base_url,mail=email_to).send_mail(self.id)
    
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
                        
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
                        email_to = next_approver.work_email  
                        template = self.env.ref('hr_holidays_multi_levels_approval.hr_leave_approved_email_template', False)
                        template_id = self.env['mail.template'].browse(template.id)
                        template_id.with_context(url=base_url,mail=email_to).send_mail(self.id)
                        
            if is_last_approbation:
                holiday.action_validate()
            else:
                holiday.write({'state': 'confirm', 'pending_approver': next_approver.id})
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
    
    @api.model
    def create(self, vals):
        result = super(Holidays, self).create(vals)
        return result
    