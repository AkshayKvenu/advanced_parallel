

from odoo import api, fields, models, _

class HrLeaveAllocationAccrualBalanceCalculator(models.TransientModel):
    _inherit = 'hr.leave.allocation.accrual.calculator'
    
    @api.model
    def _get_default_employee(self):
        if self.env.context.get('active_model') == 'employee.eos':
            return True
               
    employee_eos = fields.Boolean('Is employee eos?', default=_get_default_employee)
    
    balance_copy = fields.Float(string="Balance copy")
    
    @api.model
    def default_get(self, field_list):
        res = super(HrLeaveAllocationAccrualBalanceCalculator, self).default_get(field_list)
        if self.env.context.get('active_model') == 'employee.eos':
            eos_obj = self.env['employee.eos']
            employee_eos = eos_obj.browse(self._context.get('active_ids'))[0]
            for vals in employee_eos:
                if vals.relieving_date:
                    res.update({
                        'date': vals.relieving_date})
                    
        return res 
           
    @api.onchange('balance')
    def balance_onchange(self):
        self.balance_copy = self.balance
        
    def save_method(self):
        eos_obj = self.env['employee.eos']
        employee_eos = eos_obj.browse(self._context.get('active_ids'))[0]
        for vals in self:
            employee_eos.write({'balance': vals.balance_copy})
        