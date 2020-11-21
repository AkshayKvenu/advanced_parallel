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
    'name': "Invoice Arabic Report",

    'version': '2.2',
    'category': 'Accounting',
    'summary': 'Invoices,proforma,payment receipt',
    'description': """
        Arabic Report for Invoice in Odoo 11.
        """,
    'author': 'Amzsys',
    'website': 'http://amzsys.com/',
    'depends': [
         'account',
         'advanced_lines_sale'
    ],
    'data': [
#         'report/report_inherit_layout_templates.xml',
        'report/invoice_arabic_report_templates.xml',
        'report/invoice_rental_report_templates.xml',
#         'report/purchase_order_report_templates.xml',
#         'report/sale_order_report_templates.xml',
#         'report/delivery_note_report_templates.xml',
#         'views/res_company_view.xml',
#         'views/account_view.xml',
        'views/report_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: