# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
  
  
    @api.model
    def create(self, vals):
        if self.env['ir.config_parameter'].sudo().get_param('purchase_invoice_terms.invoice_note'):
            vals['comment'] = self.env['ir.config_parameter'].sudo().get_param('purchase_invoice_terms.invoice_note')
        result = super(AccountInvoice, self).create(vals)
        return result
    
    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.env['ir.config_parameter'].sudo().get_param('purchase_invoice_terms.invoice_note'):
            vals = self.env['ir.config_parameter'].sudo().get_param('purchase_invoice_terms.invoice_note')
            self.update({
                'comment': vals,})
            
            
             