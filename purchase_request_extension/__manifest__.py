# -*- coding: utf-8 -*-
{
    'name': "purchase_request_extension",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '20.4',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase_request','advanced_lines_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/purchase_request_line_make_purchase_order_view.xml',
        'views/purchase_request_view.xml',
        'report/pruchase_request_report_view.xml',
    ],
}