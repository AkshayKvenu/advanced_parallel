# -*- coding: utf-8 -*-
{
    'name': "Purchase Invoice Terms",

    'summary': """
        Default terms and condition for purchase and invoice """,

    'description': """
        Can add default Terms and condition for purchase and invoice 
        and will automatically update while creating purchase or invoice records.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/purchase.xml',
    ],
 
}