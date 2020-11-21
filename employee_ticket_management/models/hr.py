# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from _datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class HrContract(models.Model):
    _inherit = 'hr.contract'
    
    leave_period = fields.Selection(string='Leave Period',selection=[('yearly', 'Yearly'), ('2_years', '2 Years')],default='yearly')  
    

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    @api.multi
    def open_resume_date(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('employee_ticket_management', 'hr_employee_resume_action')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, group_by=False),
            domain=[('employee_id', '=', self.id)]
        )
        return res
    
    @api.multi
    def open_tickets(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window'].for_xml_id('employee_ticket_management', 'vacation_leave_action')
        res.update(
            context=dict(self.env.context, default_employee_id=self.id, group_by=False),
            domain=[('employee_id', '=', self.id)]
        )
        return res
    
    def create_ticket(self,emp,date):
        self.env['employee.vacation.ticket'].create(
            {
                'employee_id' : emp.id,
                'depart_on' : date,
                
                }
            )

    def get_leave_date(self,period):
        if period > 0:
            return date.today() - relativedelta(years=period)
        else :
            return False 
                                                       
            
        
    def get_employee_leave_period(self,emp):
        contract = self.env['hr.contract'].search([('employee_id','=',emp.id),('state','=','open')],limit=1)
        if contract.leave_period == 'yearly':
            return 1
        elif contract.leave_period == '2_years':
            return 2
        else :
            return 0
     
    @api.multi   
    def action_vacation_ticket(self):
        emp_obj = self.env['hr.employee'].search([])
        for emp in emp_obj:
            leave_period = self.get_employee_leave_period(emp)
            date_check = self.get_leave_date(leave_period)
            emp_resume_obj = self.env['hr.employee.resume'].search([('employee_id','=',emp.id)],order="resume_date desc",limit=1)
            emp_ticket_obj = self.env['employee.vacation.ticket'].search([('employee_id','=',emp.id)],order="create_date desc",limit=1)
            if date_check:
                if not emp_ticket_obj or emp_ticket_obj.create_date.date() < date_check:
                    if emp_resume_obj:
                        if emp_resume_obj.resume_date < date_check:
                            self.create_ticket(emp,emp_resume_obj.resume_date)
                                
    #                         elif emp_ticket_obj.create_date.date() < date_check:
    #                             self.create_ticket(emp,emp_resume_obj.resume_date)
                    
                    else :
                        if emp.joining_date:
                            if emp.joining_date <= date_check:
                                self.create_ticket(emp,emp.joining_date)
    #                             elif emp_ticket_obj.create_date.date() < date_check:
    #                                 self.create_ticket(emp,emp.joining_date)
                        
    
class HrEmployeeResume(models.Model):
    _name = 'hr.employee.resume'
    _rec_name = 'employee_id'
    
    def compute_employee(self):
        active_id=self.env.context.get('active_id')
        return self.env['hr.employee'].browse(active_id)        
    
    employee_id = fields.Many2one('hr.employee','Name', default=lambda self:self.compute_employee())
    leave_id = fields.Many2one('hr.leave',string="Leave")
    resume_date = fields.Date("Resume Date")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], default='draft') 

    def onchange_get_domain_leave(self):
        if self.employee_id:
            obj=self.search([('state','=','confirm')])
            available_ids=[i.leave_id.id for i in obj]
            ticket_obj = self.env['employee.vacation.ticket'].search([('employee_id','=',self.employee_id.id),('state','=','confirm')])
            ticket_leave_ids=[i.leave_id.id for i in ticket_obj if i.leave_id.id not in available_ids]
            self.leaves_ids=ticket_leave_ids

    leaves_ids = fields.Many2many('hr.leave', compute='onchange_get_domain_leave')
    
    
    def action_confirm_ticket(self):
        resume_obj = self.env['hr.employee.resume'].search([('leave_id','=',self.leave_id.id),('state','=','confirm'),('id','!=',self.id)])
        if resume_obj:
            raise ValidationError(_("This leave is already allocated to some other resume so please check"))
            
        self.state = 'confirm'
        
    def action_cancel_ticket(self):
        self.state = 'draft'
    
    @api.onchange('employee_id')
    def _get_domain_(self):
        obj=self.search([('state','=','confirm')])
        available_ids=[i.leave_id.id for i in obj]
        ticket_obj = self.env['employee.vacation.ticket'].search([('employee_id','=',self.employee_id.id),('state','=','confirm')])
        ticket_leave_ids=[i.leave_id.id for i in ticket_obj if i.leave_id.id not in available_ids]
        self.leaves_ids=ticket_leave_ids
    
    
        