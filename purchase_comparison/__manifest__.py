# -*- coding: utf-8 -*-
{
    'name': "purchase_comparison",

    'summary': """
        To compare multiple purchase orders (RFQ / Request for Quotation to Vendor) """,

    'description': """
        To compare multiple purchase orders (RFQ / Request for Quotation to Vendor) 
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.20.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/purchase.xml',
        'wizard/purchase_wizard.xml',
    ],
    # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
}