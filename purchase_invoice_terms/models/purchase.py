# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "purchase.order"
  
    
    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param('purchase_invoice_terms.purchase_note') or ''
    
    note = fields.Text('Terms and Conditions', default=_default_note)