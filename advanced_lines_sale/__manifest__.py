# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) © 2019 KITE.
# (http://kite.com.sa)
# info@kite.com.sa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see .
#
##############################################################################

{
    'name': 'Sales Customizations',
    'version': '1.20.5',
    'category': 'Sales',
    'sequence': 5,
    'summary': 'Sales Customizations for Advanced Lines',
    'description': '''
            Sales Customizations for Advanced Lines.
    ''',
    'website': 'http://kite.com.sa',
    'author' : 'KITE',
    'depends': ['sale', 'account', 'product', 'purchase', 'sale_timesheet', 'stock','repair', 'report_xlsx',
                 'kanban_draggable', 'project_task_default_stage', 'account_analytic_parent'],
    'data' :[  
                'security/advanced_lines_security.xml',
                'security/ir.model.access.csv',
                'wizard/add_timesheet_view.xml',
                'wizard/sale_make_invoice_advance_views.xml',
                'wizard/timesheet_report_wizard_view.xml',
                'data/email_confirm_sent.xml',
                'data/ir_sequence_data.xml',
                'data/report_html_cron_data.xml',
                'views/product_view.xml',
                'views/sale_order_view.xml',
                'views/project_task_view.xml',
                'views/stock_move_view.xml',
                'views/stock_picking_view.xml',
                'views/account_view.xml',
                'views/partner_view.xml',
                'views/purchase_view.xml',
                'views/res_config_view.xml',
                'views/payment_voucher_view.xml',
                'views/uom_view.xml',
                'views/repair_view.xml',
                'report/sale_report_templates.xml', 
                'report/invoice_report_templates.xml',  
                'report/payment_voucher_report.xml',
                'report/purchase_order_report.xml',
#                 'report/invoice_rental_report_templates.xml',  
                'report/report_views.xml',    

             ],
    'css': ['static/src/css/report.css'],
#     'price': 29,
#     'currency': "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

