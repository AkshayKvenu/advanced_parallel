# -*- coding: utf-8 -*-
from odoo import http

# class AdvancedLineSaleMrp(http.Controller):
#     @http.route('/advanced_line_sale_mrp/advanced_line_sale_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/advanced_line_sale_mrp/advanced_line_sale_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('advanced_line_sale_mrp.listing', {
#             'root': '/advanced_line_sale_mrp/advanced_line_sale_mrp',
#             'objects': http.request.env['advanced_line_sale_mrp.advanced_line_sale_mrp'].search([]),
#         })

#     @http.route('/advanced_line_sale_mrp/advanced_line_sale_mrp/objects/<model("advanced_line_sale_mrp.advanced_line_sale_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('advanced_line_sale_mrp.object', {
#             'object': obj
#         })