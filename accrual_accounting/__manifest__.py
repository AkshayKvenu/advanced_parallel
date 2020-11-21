# -*- coding: utf-8 -*-
{
    'name': "accrual_accounting",

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
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'data/move_post_cron.xml',
        'security/accrual_accounting_security.xml',
        'security/ir.model.access.csv',
        'wizard/modify_expenses_view.xml',
        'wizard/modify_revenues_views.xml',
        'wizard/related_purchase_wizard_views.xml',
        'views/accrual_expenses_views.xml',
        'views/accrual_revenues_views.xml',
        'views/account_move_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}