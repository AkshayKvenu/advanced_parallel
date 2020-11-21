# -*- coding: utf-8 -*-
{
    'name': "Asset Overhauling",

    'summary': """Asset Overhauling""",

    'description': """
        Asset Overhauling
    """,

    'author': "KITE",
    'website': "http://kite.com.sa",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','om_account_asset'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/asset_revaluate_wizard_view.xml',
        'views/account_asset_views.xml',
    ],
}