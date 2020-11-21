# -*- coding: utf-8 -*-
from odoo import http

# class PartnerNoCreateEdit(http.Controller):
#     @http.route('/partner_no_create_edit/partner_no_create_edit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_no_create_edit/partner_no_create_edit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_no_create_edit.listing', {
#             'root': '/partner_no_create_edit/partner_no_create_edit',
#             'objects': http.request.env['partner_no_create_edit.partner_no_create_edit'].search([]),
#         })

#     @http.route('/partner_no_create_edit/partner_no_create_edit/objects/<model("partner_no_create_edit.partner_no_create_edit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_no_create_edit.object', {
#             'object': obj
#         })