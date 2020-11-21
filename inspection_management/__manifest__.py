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
    'name': 'Equipment Inspection Management',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Equipment Inspection management for Advanced Lines',
    'description': '''
            Equipment Inspection management for Advanced Lines.
    ''',
    'website': 'http://kite.com.sa',
    'author' : 'KITE',
    'depends': ['stock', 'advanced_lines_sale'],
    'data' :[  
                'security/ir.model.access.csv',
#                 'wizard/add_timesheet_view.xml',
#                 'wizard/sale_make_invoice_advance_views.xml',
                'data/inspection_data.xml',
                'data/service_cron_reverse.xml',
                'views/inspection_view.xml',
                'views/stock_move_views.xml',
                'views/product_view.xml',
#                 'views/sale_order_view.xml',
#                 'views/project_task_view.xml',
#                 'views/stock_move_view.xml',
#                 'views/account_view.xml',
#                 'report/sale_report_templates.xml',                

             ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

