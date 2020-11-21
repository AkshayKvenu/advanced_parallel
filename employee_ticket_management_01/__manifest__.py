# -*- coding: utf-8 -*-
{
    'name': "employee_ticket_management",

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
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_holidays','account','hr_contract','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security_vacation_ticket.xml',
        'security/ir.model.access.csv',
        'data/hr_vacation_tickect_cron.xml',
        'data/ir_sequence_data.xml',
        'views/hr_contract_view.xml',
        'views/hr_employee_resume_views.xml',
        'views/hr_employee_views.xml',
        'views/vacation_ticket_view.xml',
#         'views/account.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}