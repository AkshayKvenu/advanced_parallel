# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2016 Amzsys IT Solutions Pvt Lt
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
    'name': 'Saudi Payroll Allowances',
    'version': '1.13.20.1',
    'category': 'hr',
    'summary': 'Saudi Payroll Allowances',
    'description':'Saudi Payroll Allowances',
    'author':'Amzsys',
    'website': 'www.amzsys.com',
    'depends': [
                'hr_payroll',
                'hr_attendance',
                'employee_document_management',
                'hr_holidays',
                'hr_contract',
                'account',
            ],
    'data': [
                'security/saudi_payroll_security.xml',
                'security/ir.model.access.csv',
                'views/hr_views.xml',
                'views/hr_payslip_views.xml',
                'report/payslip_report.xml',
                'data/payslip_mail.xml',   
             ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


