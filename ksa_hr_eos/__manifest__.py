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
    'name': 'Employee EOS',
    'version': '1.6.20.1',
    'category': 'HR',
    'sequence': 5,
    'summary': 'Employee End of Service Calculations',
    'description': """

====================================================


""",
    'author': 'Amzsys',
    'website': 'http://amzsys.com/',
    'depends': [
        'base','hr','hr_payroll','hr_contract'
    ],
    'data': [
        'security/employee_eos_security.xml',
        'security/ir.model.access.csv',
        'data/salary_rule.xml',
        'wizard/eos_view.xml',
        'views/hr_views.xml',
        'views/report_view.xml',
        'report/eos_report.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: