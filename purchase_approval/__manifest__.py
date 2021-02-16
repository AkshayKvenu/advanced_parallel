# -*- coding: utf-8 -*-
{
    'name': "purchase_approval",

    'summary': """
        Purchase Order Approval, Request for approval mail and approved mail""",

    'description': """
        Purchase Order Approval, Request for approval mail and approved mail
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.20.5',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase_order_approved','mail','purchase','advanced_lines_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'report/purchase_order_report.xml',
        'views/res_company.xml',
        'views/purchase_order.xml',
        'data/confirm_mail.xml',
        'data/approve_mail.xml',
        'views/config_settings.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}