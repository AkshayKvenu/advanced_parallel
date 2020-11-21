# -*- coding: utf-8 -*-
{
    'name': "visa_management",

    'summary': """
        This module deals with the visa management of employees""",

    'description': """
        This module deals with the visa management of employees
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.20.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail','saudi_payroll_allowances',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}