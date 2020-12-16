# -*- coding: utf-8 -*-
{
    'name': "Fleet Document Management",

    'summary': """
        'Fleet Documents, Expiring Notifications',""",

    'description': """
====================================================
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2.20.2',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet'],

    # always loaded
    'data': [
        'security/security_fleet_document.xml',
        'security/ir.model.access.csv',
        'data/fleet_document_data.xml',
        'views/fleet_document_views.xml',
        'views/fleet_vehicle_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}