# -*- coding: utf-8 -*-
from odoo import http

# class EmployeeTicketManagement(http.Controller):
#     @http.route('/employee_ticket_management/employee_ticket_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_ticket_management/employee_ticket_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_ticket_management.listing', {
#             'root': '/employee_ticket_management/employee_ticket_management',
#             'objects': http.request.env['employee_ticket_management.employee_ticket_management'].search([]),
#         })

#     @http.route('/employee_ticket_management/employee_ticket_management/objects/<model("employee_ticket_management.employee_ticket_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_ticket_management.object', {
#             'object': obj
#         })