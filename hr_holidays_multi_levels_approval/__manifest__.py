# -*- encoding: utf-8 -*-
# Baamtu, 2017
# GNU Affero General Public License <http://www.gnu.org/licenses/>
{
    "name" : "Holidays multi levels approval",
    "version" : "12.4.20.2",
    'license': 'AGPL-3',
    "author" : "Amzsys",
    "category": "Generic Modules/Human Resources",
    'website': 'http://www.baamtu.com/',
    'images': ['static/description/banner.jpg'],
    'depends' : ['hr', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/rejection_wizard.xml',
        'views/employee.xml',
        'views/holidays.xml',
        'views/company.xml',
        'data/approve_request_mail.xml',
        'data/approved_mail.xml',
        'data/rejection_mail.xml',
        'data/hr_approval_mail.xml',
#         'report/leave_report.xml',
        ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
