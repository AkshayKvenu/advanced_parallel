# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    tax_validation = fields.Selection([('warn', 'A warning message when tax id is duplicated'),
                                        ('block', 'A blocking message when tax id is duplicated')],
                                       'Tax id validation')

    
    
    @api.model
    def get_values(self):
        res = super(ResConfig, self).get_values()
        default_tax_validation = self.env['ir.config_parameter'].sudo().get_param('vat_number_duplication.tax_validation')
        
        res.update(
            {'tax_validation': default_tax_validation}
        )
        return res
 
    @api.multi
    def set_values(self):
        res = super(ResConfig, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
 
        default_tax_validation = self.tax_validation
          
        param.set_param('vat_number_duplication.tax_validation', default_tax_validation)
        return res
