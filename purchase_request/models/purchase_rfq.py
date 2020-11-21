from odoo import api, fields, models

class PurchaseRFQ(models.Model):
    _inherit = 'purchase.order'
    
    source_document = fields.Char('Source Document')
    
#     @api.multi
#     def make_purchase_order(self):
#         res = super(PurchaseRFQ, self).make_purchase_order()
#        
#        