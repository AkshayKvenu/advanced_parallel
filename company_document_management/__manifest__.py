# -*- coding: utf-8 -*-
{
    'name': "company_document_management",

    'summary': 'Company Documents, Expiring Notifications',

    'description': """
====================================================
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.4.20.1',
    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail','employee_document_management'],

    # always loaded
    'data': [
        'data/company_document_data.xml',
        'security/company_document.xml',
        'security/ir.model.access.csv',
        'views/admin_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}