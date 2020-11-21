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
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
import datetime
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _


class CompanyAdmin(models.Model):
    _name = 'admin.company'
    _rec_name = 'name'

    name = fields.Char(string='Document Name')
    user_id = fields.Many2many('res.users', string='Responsible')
    reminder_before = fields.Integer(string='Remind Before How many days')   
    

class AdminTags(models.Model):
    _name = 'admin.tags'
    
    name = fields.Char('Name')

class DocumentAdmin(models.Model):
    _name = 'admin.document'
    _inherit = 'mail.thread'
    _rec_name = 'cost_sub_type_id'
    
    def _compute_next_year_date(self, strdate):
        oneyear = relativedelta(years=1)
        start_date = fields.Date.from_string(strdate)
        return fields.Date.to_string(start_date + oneyear)
    
    @api.model
    def _default_company(self):
        return self.env['res.company']._company_default_get('company.document.management')
    
    cost_sub_type_id = fields.Many2one('admin.company', 'Document Name',required=True, track_visibility='onchange', help='Cost type purchased with this cost')
    document = fields.Char(string="Document #", track_visibility='onchange')
    company_id = fields.Many2one(comodel_name='res.company', string='Company', track_visibility='onchange', index=1,default=_default_company, readonly=True)
    active = fields.Boolean(default=True)
    date = fields.Date(default=fields.Date.context_today, track_visibility='onchange')
    start_date = fields.Date('Start Date', track_visibility='onchange', default=fields.Date.context_today, help='Date when the coverage of the contract begins')
    expiration_date = fields.Date('Expiration Date', track_visibility='onchange', default=lambda self: self._compute_next_year_date(fields.Date.context_today(self)),
        help='Date when the coverage of the contract expirates (by default, one year after begin date)')
    next_reminder = fields.Datetime(string="Reminder Date", track_visibility='onchange')
    mail_time = fields.Datetime(string='Mail Send Time', track_visibility='onchange', readonly=True)
    user_ids = fields.Many2many('res.users', string="Remind To", track_visibility='onchange')
    admin_tags_ids = fields.Many2many('admin.tags', string="Tags", track_visibility='onchange')
    ins_ref = fields.Char('Invoice Reference', track_visibility='onchange', size=64, copy=False)
    days_left = fields.Integer(compute='_compute_days_left_', string='Warning Date', track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Valid'), ('renew', 'Near Expire'), ('expired', 'Expired'), ('closed', 'Terminated')],
                              'Status', default='draft', readonly=True, help='Choose wheter the contract is still valid or not',
                              copy=False, track_visibility='onchange')
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments", track_visibility='onchange')
    history_ids = fields.One2many('admin.document.contract.history','contract_history_id', track_visibility='onchange')
    notes = fields.Text('Terms and Conditions', help='Write here all supplementary information relative to this contract', track_visibility='onchange', copy=False)
    
    
    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_("You can delete a record only in draft state."))
        res = super(DocumentAdmin, self).unlink()
        return res
    
    @api.depends('expiration_date', 'state')
    def _compute_days_left_(self):
        """return a dict with as value for each contract an integer
        if contract is in an open state and is overdue, return 0
        if contract is in a closed state, return -1
        otherwise return the number of days before the contract expires
        """
        for record in self:
            if (record.expiration_date and record.state == 'open'):
                today = fields.Date.from_string(fields.Date.today())
                renew_date = fields.Date.from_string(record.expiration_date)
                diff_time = (renew_date - today).days
                record.days_left = diff_time > 0 and diff_time or 0
            else:
                record.days_left = -1
    
    def _action_send_expiry_mail(self):
        template = self.env.ref('company_document_management.email_template_company_document_expiry_mail', False)
        if not template:
            raise UserError(_('The Forward Email Template is not in the database'))
        local_context = self.env.context.copy()
        template.with_context(local_context).send_mail(self.id, force_send=True)
        self.write({
            'state': 'expired',
            'mail_time': datetime.datetime.now()
        })
    
    def _action_send_reminder_mail(self):
        template = self.env.ref('company_document_management.email_template_company_document_reminder_mail', False)
        if not template:
            raise UserError(_('The Forward Email Template is not in the database'))
        local_context = self.env.context.copy()
        template.with_context(local_context).send_mail(self.id, force_send=True)
        self.write({
            'state': 'renew',
            'mail_time': datetime.datetime.now()
        })
    
    @api.multi
    def action_draft(self):
        for record in self:
            if not record.expiration_date or not record.start_date:
                raise ValidationError(_("Start date and Expiration date cannot be null."))
            
            today = fields.Date.today()
            if record.expiration_date <= today:
                record._action_send_expiry_mail()
            elif record.next_reminder:
                if record.next_reminder.date() <= today:
                    record._action_send_reminder_mail()
                else:
                    record.state = 'open'
            else:
                record.state = 'open'
    
    @api.multi
    def contract_close(self):
        for record in self:
            record.state = 'closed'
    
    @api.multi
    def contract_open(self):
        for record in self:
            record.state = 'draft'
            
    @api.multi
    def act_renew_contract_(self):
        
        self.write({'history_ids':[(0,0,{'start_date':self.start_date,'expiration_date':self.expiration_date,'next_reminder':self.next_reminder,
                                                                              'date':self.date, 'ins_ref': self.ins_ref})]})
        
        
        self.write({'state': 'draft','ins_ref': False, 'next_reminder':False, 'date':False, 'expiration_date':False,
                     'start_date':False, 'mail_time':False})
    
    
    @api.constrains('start_date', 'expiration_date')
    def _check_dates(self):
        if (('start_date' == True) and ('expiration_date' == True)):
            if any(self.filtered(lambda document: document.start_date > document.expiration_date)):
                raise ValidationError(_("Document 'Issue Date' must be before 'Date Expiry'."))
    
    @api.onchange('cost_sub_type_id')
    def onchange_cost_subtype_id(self):
        if self.cost_sub_type_id:
            self.user_ids = self.cost_sub_type_id.user_id.ids
    
    @api.onchange('expiration_date', 'cost_sub_type_id','cost_sub_type_id.reminder_before')
    def onchange_date_issue_expiry(self):
#         if any(self.filtered(lambda document: document.start_date > document.expiration_date)):
#             raise ValidationError(_("Document 'Issue Date' must be before 'Date Expiry'."))
        from_dt = fields.Date.from_string(self.start_date)
        to_dt = fields.Date.from_string(self.expiration_date)
        if from_dt and to_dt:
            time_delta = to_dt - from_dt
            if time_delta.days > self.cost_sub_type_id.reminder_before:
                to_dt -= datetime.timedelta(days=self.cost_sub_type_id.reminder_before)
                self.next_reminder = str(to_dt)
            else:
                self.next_reminder = str(fields.Date.today())
    
    @api.multi
    def set_as_pending(self):
        today_date = fields.Date.today()
        emp_rec = self.env['admin.document'].search([])
        for rec in emp_rec:
            if rec.next_reminder and rec.state != 'closed':
                dt = datetime.datetime.strptime(str(rec.next_reminder),'%Y-%m-%d %H:%M:%S')
                if dt.date() == today_date and rec.state == 'open':
                    rec.state = 'renew'
    
    @api.multi
    def set_as_close(self):
        today_date = fields.Date.today()
        company_rec = self.env['admin.document'].search([('state', 'in', ['open', 'renew'])])
        for rec in company_rec:
            if rec.expiration_date:
                if rec.expiration_date == today_date:
                    rec._action_send_expiry_mail()
    
    @api.multi
    def get_partner_ids(self, user_ids):
        return str([user.partner_id.id for user in user_ids]).replace('[', '').replace(']', '') 
    
    @api.multi              
    def action_sendmail(self):
        today_date = fields.Date.today()
        emp_rec = self.env['admin.document'].search([('state', '=', 'open')])
        for rec in emp_rec:
            if rec.next_reminder:
                dt = datetime.datetime.strptime(str(rec.next_reminder), '%Y-%m-%d %H:%M:%S')
                if dt.date() == today_date:
                    rec._action_send_reminder_mail()
#                     template = self.env.ref('company_document_management.email_template_company_document_reminder_mail', False)
#                     if not template:
#                         raise UserError(_('The Forward Email Template is not in the database'))
#                     local_context = self.env.context.copy()
#                     template.with_context(local_context).send_mail(rec.id, force_send=True)
#                     rec.state = 'renew'
#                     rec.mail_time = datetime.datetime.now()
    
class CompanyContractHistory(models.Model):
    _name = "admin.document.contract.history"
    contract_history_id = fields.Many2one('admin.document')
    
    start_date = fields.Date('Start Date')
    expiration_date = fields.Date('Expiration Date')
    next_reminder = fields.Datetime(string="Reminder Date")
    date = fields.Date("Invoice Date")
    ins_ref = fields.Char('Invoice Reference')    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: