# -*- coding: utf-8 -*-
{
    'name': "Select Amortization",

    'summary': """Select Amortization""",

    'description': """
        Select Amortization
    """,

    'author': "KITE",
    'website': "http://kite.com.sa",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.20.3',

    # any module necessary for this one to work correctly
    'depends': ['base','account','hr_expense'],

    # always loaded
    'data': [
        'security/security_amortization.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/account_asset_data.xml',
    ],
}
