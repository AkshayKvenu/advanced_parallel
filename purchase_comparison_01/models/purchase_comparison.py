# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class PurchaseComparison(models.Model):
    _name = "purchase.compare"
    _auto = False
    _rec_name = 'id'

    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Vendor', readonly=True)
    unit_quantity = fields.Float('Product Quantity', readonly=True)
    price_total = fields.Float('Total Price', readonly=True)
    
        
    @api.model_cr
    def price_compare(self):
        active_ids = self._context.get('active_ids', [])
       
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        
        sql = """CREATE or REPLACE VIEW purchase_compare as (SELECT min(pol.id) as id, pol.product_id, pol.name, SUM(pol.product_qty)
             AS unit_quantity, SUM(pol.price_subtotal) AS price_total, po.partner_id FROM 
             purchase_order_line pol INNER JOIN purchase_order po ON pol.order_id=po.id
            join res_partner partner on po.partner_id = partner.id
            left join product_product p on (pol.product_id=p.id) 
            WHERE po.id IN %s  
            GROUP BY pol.product_id, pol.name, po.partner_id)"""
         
        params = (tuple(active_ids),)
        return self.env.cr.execute(sql, params)

    
