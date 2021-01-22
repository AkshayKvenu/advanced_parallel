# -*- coding:utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class Holidays(models.Model):
    _name = "hr.leave"
    _inherit = "hr.leave"
    
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved'),
        ('hr_approval', 'HR Approval')
        ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
        help="The status is set to 'To Submit', when a leave request is created." + 
        "\nThe status is 'To Approve', when leave request is confirmed by user." + 
        "\nThe status is 'Refused', when leave request is refused by manager or approvers." + 
        "\nThe status is 'Approved', when leave request is approved by manager." + 
        "\nThe status is 'HR Approval', when leave request is approved by all approvers.")
    
    rejection_reason = fields.Text(string="Rejection Reason")
    
    def _default_approver(self):
        employee = self._default_employee()
        if employee.holidays_approvers:
                return employee.holidays_approvers[0].approver.id

    pending_approver = fields.Many2one('hr.employee', string="Pending Approver", readonly=True, default=_default_approver)
    pending_approver_user = fields.Many2one('res.users', string='Pending approver user', related='pending_approver.user_id', related_sudo=True, store=True, readonly=True)
    current_user_is_approver = fields.Boolean(string='Current user is approver', compute='_compute_current_user_is_approver')
    approbations = fields.One2many('hr.employee.holidays.approbation', 'holidays', string='Approvals', readonly=True)
    pending_transfered_approver_user = fields.Many2one('res.users', string='Pending transfered approver user', compute="_compute_pending_transfered_approver_user", search='_search_pending_transfered_approver_user')
    
    
    @api.multi
    def action_confirm(self):
        super(Holidays, self).action_confirm()
        for holiday in self:
            if holiday.employee_id.holidays_approvers:
                holiday.pending_approver = holiday.employee_id.holidays_approvers[0].approver.id
                
                if holiday.pending_approver:
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
                    email_to = holiday.pending_approver.work_email  
                    template = self.env.ref('hr_holidays_multi_levels_approval.hr_leave_approve_request_email_template', False)
                    template_id = self.env['mail.template'].browse(template.id)
                    template_id.with_context(url=base_url, mail=email_to).send_mail(self.id, force_send=True)
        return True
    
    
    @api.multi
    def action_validate(self):
        
        is_officer = self.env.user.has_group('hr_holidays.group_hr_holidays_user')
        is_manager = self.env.user.has_group('hr_holidays.group_hr_holidays_manager')
        
        self.write({'pending_approver': None})
        for holiday in self:
            self.env['hr.employee.holidays.approbation'].create({'holidays': holiday.id, 'approver': self.env.uid, 'date': fields.Datetime.now()})
            
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        if any(holiday.state not in ['confirm', 'validate1', 'hr_approval'] for holiday in self):
            raise UserError(_('Leave request must be confirmed in order to approve it.'))
        
        if is_manager:
            self.write({'state': 'validate'})
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
            lang = self.env.user.lang
#             email_to = self.employee_id.company_id.email_notification_ids
            template = self.env.ref('hr_holidays_multi_levels_approval.hr_approved_email_template', False)
            template_id = self.env['mail.template'].browse(template.id)
            template_id.with_context(url=base_url, lang=lang).send_mail(self.id, force_send=True)
                        
        else:
            self.write({'state': 'hr_approval'})
            
        self.filtered(lambda holiday: holiday.validation_type == 'both').write({'second_approver_id': current_employee.id})
        self.filtered(lambda holiday: holiday.validation_type != 'both').write({'first_approver_id': current_employee.id})
 
        for holiday in self.filtered(lambda holiday: holiday.holiday_type != 'employee'):
            if holiday.holiday_type == 'category':
                employees = holiday.category_id.employee_ids
            elif holiday.holiday_type == 'company':
                employees = self.env['hr.employee'].search([('company_id', '=', holiday.mode_company_id.id)])
            else:
                employees = holiday.department_id.member_ids
 
            if self.env['hr.leave'].search_count([('date_from', '<=', holiday.date_to), ('date_to', '>', holiday.date_from),
                               ('state', 'not in', ['cancel', 'refuse']), ('holiday_type', '=', 'employee'),
                               ('employee_id', 'in', employees.ids)]):
                raise ValidationError(_('You can not have 2 leaves that overlaps on the same day.'))
 
            values = [holiday._prepare_holiday_values(employee) for employee in employees]
            leaves = self.env['hr.leave'].with_context(
                tracking_disable=True,
                mail_activity_automation_skip=True,
                leave_fast_create=True,
            ).create(values)
            leaves.action_approve()
            # FIXME RLi: This does not make sense, only the parent should be in validation_type both
            if leaves and leaves[0].validation_type == 'both':
                leaves.action_validate()
 
        employee_requests = self.filtered(lambda hol: hol.holiday_type == 'employee')
        employee_requests._validate_leave_request()
        if not self.env.context.get('leave_fast_create'):
            employee_requests.activity_update()
        return True
    
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
                        if next_approver:
                            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                            base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
                            email_to = next_approver.work_email
                            template = self.env.ref('hr_holidays_multi_levels_approval.hr_leave_approved_email_template', False)
                            template_id = self.env['mail.template'].browse(template.id)
                            template_id.with_context(url=base_url, mail=email_to).send_mail(self.id, force_send=True)
                        
            if is_last_approbation:
                group = self.env['res.groups'].sudo().search([('name','=','Manager'),('category_id.name','=','Leaves')],limit=1)
                email_list = []
                for vals in group.users:
                    email_to = vals.partner_id.email
                    email_list.append(email_to)
                    email_list_new = ','.join( c for c in email_list if c not in "[]''")
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
                email_to = email_list_new
                template = self.env.ref('hr_holidays_multi_levels_approval.hr_leave_approved_email_template', False)
                if template:
                    template.with_context(url=base_url, mail=email_to).send_mail(self.id, force_send=True)
                holiday.action_validate()
            else:
                holiday.write({'state': 'confirm', 'pending_approver': next_approver.id})
                self.env['hr.employee.holidays.approbation'].create({'holidays': holiday.id, 'approver': self.env.uid, 'sequence': sequence, 'date': fields.Datetime.now()})
            


    @api.one
    def _compute_current_user_is_approver(self):
        if self.pending_approver.user_id.id == self.env.user.id or self.pending_approver.transfer_holidays_approvals_to_user.id == self.env.user.id:
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
    def get_email_to(self):
        for holiday in self:
            email_list = []
            if holiday.employee_id.company_id.email_notification_ids:
                for vals in holiday.employee_id.company_id.email_notification_ids:
                    for line in vals.partner_id:
                        email_list.append(line.email)
            email_list.append(holiday.employee_id.work_email)
            new = ",".join(email_list)
        return new
            

#     @api.multi
#     def action_validate(self):
#         self.write({'pending_approver': None})
#         for holiday in self:
#             self.env['hr.employee.holidays.approbation'].create({'holidays': holiday.id, 'approver': self.env.uid, 'date': fields.Datetime.now()})
#         return super(Holidays, self).action_validate()
    

    
