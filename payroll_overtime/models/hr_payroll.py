# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError


class payroll_overtime(models.Model):
    _name = 'hr.payroll_overtime'

    name_seq = fields.Char(string='OT number', copy=False, readonly=True)
    name = fields.Char(string="Name")
    company = fields.Many2one('res.company', string="Company", readonly=True)
    created_user = fields.Many2one('res.users', string="Created User", readonly=True)
    approved_user = fields.Many2one('res.users', "Approved User", readonly=True)
    Note = fields.Char("Notes")
    state = fields.Selection([('draft', 'Draft'), ('approve', 'Waiting for Approval'), ('done', 'Done')], default='draft', string='Status')
    payroll_line_ids = fields.One2many("hr.payroll_overtime.lines", 'payroll_id', string='Payrol lines')
    
    @api.model
    def create(self, vals):
        vals['name_seq'] = self.env['ir.sequence'].next_by_code('hr.payroll_overtime') or _('New')
        result = super(payroll_overtime, self).create(vals)
        return result
            
    @api.onchange('name')
    def _onchange_name(self):
        self.created_user = self.env.user
        self.company = self.env.user.company_id
    
    def action_done(self):
        self.approved_user = self.env.user
        for rec in self.payroll_line_ids:
            rec.state='done'
        return self.write({'state' : 'done'})
    
    def action_cancel(self):
        if self.state == 'done':
            for rec in self.payroll_line_ids:
                payslip_obj = self.env['hr.payslip'].search([('employee_id', '=', rec.employee_id.id)])
                for obj in payslip_obj:
                    dates = []
                    loop_dt = obj.date_from
                    while loop_dt <= obj.date_to:
                        dates.append(loop_dt)
                        loop_dt += datetime.timedelta(days=1)
                    if rec.start_date in dates and rec.end_date in dates and obj.contract_id:
                        raise ValidationError(_("Cannot cancel records already used in payslip"))       
                    
                print("rcccccccccccccccc",payslip_obj)
        self.approved_user = False
        for rec in self.payroll_line_ids:
            rec.state ='draft'
        return self.write({'state' : 'draft'})
         
    def action_approve(self):
        if not self.payroll_line_ids:
            raise UserError(_("Should create atleast one line "))
        for rec in self.payroll_line_ids:
            rec.state = 'approve'
        return self.write({'state' : 'approve'})


class payroll_lines_ot(models.Model):
    _name = 'hr.payroll_overtime.lines'
    
    payroll_id = fields.Many2one("hr.payroll_overtime",)
    employee_id = fields.Many2one("hr.employee", string="Employee")
    start_date = fields.Date("Start date")
    end_date = fields.Date("End date")
    OT_float = fields.Float("Over time")
    state = fields.Char("State")
    Notes = fields.Char("Notes")
    
    @api.constrains('start_date', 'end_date')
    def date_validation(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if not rec.start_date.month == rec.end_date.month or not rec.start_date.year == rec.end_date.year:
                    raise ValidationError(_("Start Date and End Date should fall in same month."))
                parent_account = self.env['hr.payroll_overtime.lines'].search([('id', '!=', rec.id),('employee_id', '=', rec.employee_id.id)])
                for res in parent_account:
                    if res.payroll_id:
                        if any([rec.start_date <= res.start_date <= rec.end_date, res.start_date <= rec.start_date <= res.end_date]):
                            raise ValidationError(_("Date range already exist for %s") % rec.employee_id.name)
            if rec.OT_float == 0.0:
                raise ValidationError(_("Overtime should not be 0"))
            
