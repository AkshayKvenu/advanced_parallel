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
    'name': 'Employee Document Management',
    'version': '8.3',
    #7.1 odoo 11 emplyee documet
    #7.2 mail issue solved
    #7.4 change docname type and onchange
    #7.5 change the record rule of employee user
    #7.6 emplyee manager permissions changed
    #7.7 employee document manager access and solve the warning in creating documents
    'category': 'Sale',
    'sequence': 5,
    'summary': 'Employee Documents, Expiring Notifications',
    'description': """
====================================================
""",
    'author': 'Amzsys',
    'website': 'http://amzsys.com/',
    'depends': [
        'hr','mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/employee_doc_security.xml',
        'data/employee_document_data.xml',
#         'data/base_action_rule.xml',
        'views/hr_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
