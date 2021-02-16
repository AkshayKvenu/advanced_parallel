# Copyright 2018-2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).


from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from datetime import datetime


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"


    @api.model
    def _prepare_item(self, line):
        res = super(PurchaseRequestLineMakePurchaseOrder, self)._prepare_item(line)
        res['product_qty_copy'] = line.pending_qty_to_receive
        return res

    @api.multi
    def make_purchase_order(self):
        request_line_id = self._context['active_id']
        request_id = self.env['purchase.request.line'].browse(request_line_id).request_id
        for item in self.item_ids:
            product_qty = 0.0
            for req_line in request_id.line_ids:
                for order_line in req_line.purchase_lines:
                    if order_line.state == 'purchase' and order_line.product_id == item.product_id:
                        product_qty += order_line.product_qty
                
            
            if item.product_qty_copy - product_qty < item.product_qty:
                raise UserError(
                    _('%s product Quantity exceeds by %s.')% (item.product_id.name,item.product_qty-(item.product_qty_copy - product_qty))
                    )
                    
            
            if item.product_qty > item.product_qty_copy:
                raise UserError(
                    _('Qty should not be greater than that in Purchase Request.'))
        
            
        
        return super(PurchaseRequestLineMakePurchaseOrder, self).make_purchase_order()


class PurchaseRequestLineMakePurchaseOrderItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order.item"

    product_qty_copy = fields.Float(
        string='Copy of Quantity',
        digits=dp.get_precision('Product Unit of Measure'))
    
    keep_description = fields.Boolean(default=True)
    
#     @api.model
#     def default_get(self, field_list):
#         res = super(PurchaseRequestLineMakePurchaseOrderItem, self).default_get(field_list)
#         print("aaaaaaaaaaaaaaaaaaaaaaaaa",res)
#         res.update({
#             'keep_description': True,
#         })
#         return res


