# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools

 
class PurchaseWizard(models.TransientModel):
    _name = 'wizard.object'
    
    @api.multi
    def method_purchase_compare(self):
        purchase_order_ids = self.env['purchase.order'].browse(self._context.get('active_ids', []))   
        purchase_compare = self.env['purchase.compare']
        
        purchase_compare.price_compare()
        
        return {
            'name': 'purchase compare',
            'view_type': 'pivot',
            'view_mode': 'pivot',
            'res_model': 'purchase.compare',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': {}
            }
        