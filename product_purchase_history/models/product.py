
from odoo import api, models, fields, _


class ProductTemplate(models.Model):
    _inherit = "product.template"
    product_purchase_count = fields.Integer(string='Product purchase count',
                                           compute='_compute_product_purchase_count')

    @api.multi
    def _compute_product_purchase_count(self):
        PurchaseOrder = self.env['purchase.order.line']
        for product in self:
            product.product_purchase_count = PurchaseOrder.search_count(
                [('product_id', '=', product.product_variant_id.id)])
            
    @api.multi
    def open_entries(self):
        move_ids = []
        for product in self:
            move_ids.append(product.product_variant_id.id)
#             for depreciation_line in product:
#                 if depreciation_line.move_id:
#                     move_ids.append(depreciation_line.move_id.id)
# product_tmpl_id
        return {
        'name': _('Purchase order line'),
        'view_type': 'form',
        'view_mode': 'tree,form',
        'res_model': 'purchase.order.line',
        'view_id': False,
        'type': 'ir.actions.act_window',
        'domain': [('product_id', 'in', move_ids)],
        }