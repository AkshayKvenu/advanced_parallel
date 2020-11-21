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
    'name': 'Journal Entry Report',
    'summary': 'Journal Entry Report in Invoice, Payment and Voucher',
    'author': 'Amzsys',
    'license': 'AGPL-3',
    'website': 'http://www.amzsys.com',
    'category': 'Accounting',
    'version': '1.1',
    'depends': ['web', 'account', 'account_voucher'],
    'data': [
            'views/account_move_views.xml',
            'report/journal_entry_report_template.xml',
            'report/journal_entry_report.xml',
    ],
    'installable': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
