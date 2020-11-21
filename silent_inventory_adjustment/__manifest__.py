# -*- coding: utf-8 -*-
{
    'name': "Silent Inventory Adjustment",

    'summary': """
        This module helps to Export/Import product stock using CSV File along with all the modified changes.
    """,

    'description': """
        This module helps to Export/Import product stock using CSV File along with all the modified changes in
        Inventory Adjustment.
    """,

    'author': "Silent Infotech Pvt. Ltd.",
    'website': "https://silentinfotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',    # Warehouse
    'version': '0.1',
    'application': True,
    'license': u'OPL-1',
    
    'auto_install': False,
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_inventory.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/banner.jpg'],
}