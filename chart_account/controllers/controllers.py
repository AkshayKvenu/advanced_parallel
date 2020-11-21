# -*- coding: utf-8 -*-
from odoo import http

# class ChartAccount(http.Controller):
#     @http.route('/chart_account/chart_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/chart_account/chart_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('chart_account.listing', {
#             'root': '/chart_account/chart_account',
#             'objects': http.request.env['chart_account.chart_account'].search([]),
#         })

#     @http.route('/chart_account/chart_account/objects/<model("chart_account.chart_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('chart_account.object', {
#             'object': obj
#         })