# -*- coding: utf-8 -*-

from odoo import models, fields, api



class block_terms_invoice(models.TransientModel):
    _inherit = 'res.config.settings'

    terms_sale_config = fields.Boolean('Terms sale to invoice')
    
    
    @api.model
    def get_values(self):
        res = super(block_terms_invoice, self).get_values()
        field1 = self.env['ir.config_parameter'].sudo().get_param('block_terms_invoice.terms_sale_config')
        print("ffffffffffffff",field1)
        res.update(
            {'terms_sale_config': field1,}
        )
        return res
 
    @api.multi
    def set_values(self):
        super(block_terms_invoice, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
 
        field1 = self.terms_sale_config 
#         and self.terms_sale_config.ids or False
        
        param.set_param('block_terms_invoice.terms_sale_config', field1)
    
    
class Sale_Advance_Payment_Inv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    
    
    @api.multi
    def _create_invoice(self, order, so_line, amount):
        res = super(Sale_Advance_Payment_Inv, self)._create_invoice(order, so_line, amount)
        field1 = self.env['ir.config_parameter'].sudo().get_param('block_terms_invoice.terms_sale_config')
        print("bolllllllllllllllllllll",field1,res['comment'])
        if field1 == False:
            res['comment'] = False
        return res
        
        
        
        
        
        