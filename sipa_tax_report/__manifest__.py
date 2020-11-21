# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 Amzsys IT Solutions Pvt Ltd
#    (http://www.amzsys.com)
#    info@amzsys.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Account VAT Report",

    'version': '1.1',
    'category': 'Accounting',
    'summary': 'Invoices,proforma,payment receipt',
    'description': """
        Tax report in PDF and XLS format.
        """,
    'author': 'Amzsys',
    'website': 'http://amzsys.com/',
    'depends': [
        'account',
        'om_account_accountant',
        'report_xlsx',
    ],
    'data': [
        'wizard/tax_report_wizard_view.xml',
        'report/report_account_tax.xml',
        'views/account_vat_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: