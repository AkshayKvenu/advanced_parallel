# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError
import calendar
from datetime import date


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    sale_type = fields.Selection([('trade', 'Trading'), ('rent', 'Rental')], 'Sale Type')


    @api.model
    def default_get(self,default_fields):
        """ Compute default partner_bank_id field for 'out_invoice' type,
        using the default values computed for the other fields.
        """
        res = super(SaleAdvancePaymentInv, self).default_get(default_fields)
        context = self.env.context
        task_id = self.env['sale.order'].browse(context.get('active_ids'))
        today = date.today()
        month = 12 if today.month == 1 else today.month - 1
        year = today.year - 1 if today.month == 1 else today.year
        
        res.update({
                'start_date': today.replace(day = 1, month = month, year = year),
                'end_date': today.replace(day = calendar.monthrange(year, month)[1], month = month, year = year),
                'sale_type': task_id[0].sale_type if task_id else False,
            })
        
        return res
    
    @api.multi
    def create_invoices(self):
        if self.start_date and self.end_date and self.sale_type == 'rent' and self.advance_payment_method in ['delivered', 'all']: 
            if not self.start_date.month == self.end_date.month or not self.start_date.year == self.end_date.year:
                raise UserError(_("Start Date and End Date should fall in same month."))
            if self.start_date > self.end_date:
                raise UserError(_("Start Date should be less than End Date."))
        res = super(SaleAdvancePaymentInv, self).create_invoices()
        return res
        
        
    
