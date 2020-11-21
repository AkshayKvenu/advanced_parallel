# -*- coding: utf-8 -*-
from odoo import http

# class AccountNoCreateEdit(http.Controller):
#     @http.route('/account_no_create_edit/account_no_create_edit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_no_create_edit/account_no_create_edit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_no_create_edit.listing', {
#             'root': '/account_no_create_edit/account_no_create_edit',
#             'objects': http.request.env['account_no_create_edit.account_no_create_edit'].search([]),
#         })

#     @http.route('/account_no_create_edit/account_no_create_edit/objects/<model("account_no_create_edit.account_no_create_edit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_no_create_edit.object', {
#             'object': obj
#         })