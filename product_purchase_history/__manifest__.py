# -*- coding: utf-8 -*-
{
    'name': "Product Purchase History",

    'summary': """Product Purchase History""",

    'description': """
        Product Purchase History
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.20.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase', 'product','stock'],

    # always loaded
    'data': [
        'views/product_view.xml',
    ],
}