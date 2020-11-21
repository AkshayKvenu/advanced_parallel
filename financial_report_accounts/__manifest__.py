# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2016 Amzsys IT Solutions Pvt Ltd
# (http://www.amzsys.com)
# info@amzsys.com
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
    'name': 'Financial Reports in Accounts',
    'summary': 'Financial Reports in Accounts',
    'description':"""
        Financial Reports reference in Chart of Accounts.
    """,
    
    'author': 'Amzsys',
    'license': 'AGPL-3',
    'website': 'http://www.amzsys.com',
    'category': 'Accounting',
    'version': '1.0',
    'depends': [
        'account', 'om_account_accountant'
    ],
    
    'data': [
            'views/account_view.xml',
            
    ],
    
    'installable': True,
    'auto_install': False,
    'application': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

