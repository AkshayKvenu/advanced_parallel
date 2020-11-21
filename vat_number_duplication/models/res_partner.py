# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
  
    @api.model
    def create(self, vals):
        tax_error = self.env['ir.config_parameter'].sudo().get_param('vat_number_duplication.tax_validation')
        partner_count = 0
        if 'vat' in vals and vals['vat']:
            partner_count = self.search_count([('vat','=',vals['vat'])])
            if partner_count > 0 and tax_error:
                if tax_error == 'block':
                    raise UserError(_("Tax ID is already registered for another customer. Please verify once again."))
        result = super(ResPartner, self).create(vals)
        return result
                
    @api.model    
    @api.onchange('vat')            
    def onchange_vat_(self):
        tax_error = self.env['ir.config_parameter'].sudo().get_param('vat_number_duplication.tax_validation')
        partner_count = 0
        if self.vat:
            partner_obj = self.search([('vat','=',self.vat),('id','!=',self._origin.id)])
            partner_count = self.search_count([('vat','=',self.vat),('id','!=',self._origin.id)])
            if partner_count > 0 and tax_error:
                if tax_error == 'warn':
                    view = self.env.ref('vat_number_duplication.warning_message_wizard')
                    return {'value':{},'warning':{'title':'warning','message':'Tax ID is already registered for another customer. Are you sure you want to continue.'}}
    
    

                
    def write(self, vals):
        tax_error = self.env['ir.config_parameter'].sudo().get_param('vat_number_duplication.tax_validation')
        partner_count = 0
        if 'vat' in vals and vals['vat']:
            partner_obj = self.search([('vat','=',vals['vat']),('id','!=',self.id)])
            partner_count = self.search_count([('vat','=',vals['vat']),('id','!=',self.id)])
            if partner_count > 0 and tax_error:
                if tax_error == 'block':
                    raise UserError(_("Tax ID is already registered for another customer. Please verify once again."))
        return super(ResPartner, self).write(vals)
        