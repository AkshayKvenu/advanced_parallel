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
    'name': 'Multi-company Product',
    'version': '1.0',
    'category': 'Stock',
    'sequence': 5,
    'summary': 'Multi-company Product Access fix',
    'description': '''
            Fix of access error coming when opening lot form, because of using same product in multiple companies.
    ''',
    'website': 'http://kite.com.sa',
    'author' : 'KITE',
    'depends': ['stock', 'sale_stock', 'purchase_stock'],
    'data' :[  
#                 'security/ir.model.access.csv',
             ],
    'css': [],
#     'price': 29,
#     'currency': "EUR",
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

