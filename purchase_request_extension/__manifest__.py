# -*- coding: utf-8 -*-
{
    'name': "Purchase Request Extension",

    'summary': """
        Purchase Request Extension""",

    'description': """
        Purchase Request Extension
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '20.9',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase_request','advanced_lines_sale','purchase_approval'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security_purchase_request.xml',
        'wizard/purchase_request_line_make_purchase_order_view.xml',
        'views/purchase_request_view.xml',
        'report/pruchase_request_report_view.xml',
    ],
}