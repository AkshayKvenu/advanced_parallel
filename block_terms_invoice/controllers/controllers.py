# -*- coding: utf-8 -*-
from odoo import http

# class BlockTermsInvoice(http.Controller):
#     @http.route('/block_terms_invoice/block_terms_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/block_terms_invoice/block_terms_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('block_terms_invoice.listing', {
#             'root': '/block_terms_invoice/block_terms_invoice',
#             'objects': http.request.env['block_terms_invoice.block_terms_invoice'].search([]),
#         })

#     @http.route('/block_terms_invoice/block_terms_invoice/objects/<model("block_terms_invoice.block_terms_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('block_terms_invoice.object', {
#             'object': obj
#         })