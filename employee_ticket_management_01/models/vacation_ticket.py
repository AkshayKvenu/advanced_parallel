from odoo import models, fields, api, _
from logging import PlaceHolder
from odoo.exceptions import UserError, ValidationError


class Ticket(models.Model):
     _name = 'employee.vacation.ticket'
     _rec_name = 'employee_sequence_number'
     

     employee_id = fields.Many2one('hr.employee',string="Employee")
     leave_id = fields.Many2one('hr.leave',string="Leave")
     from_dest = fields.Char("From")
     to_dest = fields.Char("To")
     depart_on = fields.Date("Depart On")
     return_on = fields.Date("Return On")
     adults = fields.Integer("Adults")
     children = fields.Integer("Children (2-11 yrs)")
     infants = fields.Integer("Infants (Below 2 yrs)")
     total_amount = fields.Float("Total Amount")
     inv_number = fields.Char("Invoice Number")
     pnr = fields.Char("PNR")
     type = fields.Selection(string='Type',selection=[('one_way', 'One Way'), ('round_trip', 'Round Trip')],default='one_way')
     state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], default='draft') 
     employee_sequence_number = fields.Char(copy=False, readonly=True)
     
     @api.model
     def _getUserGroupId(self):
        return [('groups_id', '=', self.env.ref('module.xml_id').id)]
     
     @api.model
     def create(self, vals):
        vals['employee_sequence_number'] = self.env['ir.sequence'].next_by_code('employee.vacation.ticket') or _('New')
        result = super(Ticket, self).create(vals)
        return result
    

     def action_confirm_ticket(self):
        if not self.leave_id:
            raise ValidationError(_("Leave cannot be null"))
            
        if self.leave_id.vacation_ticket_id:
            raise ValidationError(_("This leave is already allocated to some other ticket so please check"))
        self.state = 'confirm'
        self.leave_id.vacation_ticket_id = self.id
        
        
        
     def action_cancel_ticket(self):
        self.state = 'draft'
        if self.leave_id.vacation_ticket_id:
            self.leave_id.vacation_ticket_id = False


     @api.constrains('return_on')
     def check_dates(self):
        if self.depart_on and self.return_on:
            if self.depart_on > self.return_on:
                raise ValidationError(_("Depart on should be less than Return on"))
    
    
                
class Reference(models.Model):
     _inherit = 'hr.leave'
     
     vacation_ticket_id = fields.Many2one('employee.vacation.ticket',string="Vacation Ticket")
