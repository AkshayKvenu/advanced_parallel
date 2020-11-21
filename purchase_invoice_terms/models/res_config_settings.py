# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_note = fields.Text(string="Invoice Terms & Conditions", readonly=False)
    use_invoice_note = fields.Boolean(
        string='Default Invoice Terms & Conditions')
    
    purchase_note = fields.Text(string="Purchase Terms & Conditions", readonly=False)
    use_purchase_note = fields.Boolean(
        string='Default Purchase Terms & Conditions')
    
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        default_invoice_note = self.env['ir.config_parameter'].sudo().get_param('purchase_invoice_terms.invoice_note')
        default_purchase_note = self.env['ir.config_parameter'].sudo().get_param('purchase_invoice_terms.purchase_note')
        
        res.update(
            {'invoice_note': default_invoice_note,'purchase_note': default_purchase_note,}
        )
        return res
 
    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
 
        default_invoice_note = self.invoice_note
        default_purchase_note = self.purchase_note
          
        param.set_param('purchase_invoice_terms.purchase_note', default_purchase_note)
        param.set_param('purchase_invoice_terms.invoice_note', default_invoice_note)
        
    
    