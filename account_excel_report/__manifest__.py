# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) © 2019 KITE.
# (http://kite.com.sa)
# info@kite.com.sa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see .
#
##############################################################################

{
    'name': "Account Excel Report",

    'summary': """Account Excel Report""",

    'description': """
        Excel Reports for Accounting Reports
    """,
    'website': 'http://kite.com.sa',
    'author' : 'KITE',

    'category': 'Accounting',
    'version': '1.3',

    # any module necessary for this one to work correctly
    'depends': ['base',
        'account',
        'report_xlsx',
        'om_account_accountant',
        'web',
        'accounting_pdf_reports',
     ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/account_report_general_ledger_view.xml',
        'wizard/account_report_partner_ledger_view.xml',
        'wizard/account_report_trial_balance_view.xml',
        'wizard/account_report_financial_view.xml',
        'views/report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
