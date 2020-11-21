{
    'name': 'payroll report in excel',
    'version': '1.2',
    'category': 'payroll',
    'sequence': 60,
    'summary': 'shows the payroll report in xlsx format',
    'description': "It shows payroll report in excel for given month",
    'author':'aswathy',
    'depends': ['base','hr', 'hr_payroll'],
    'data': ['wizard/payroll_report_wiz.xml'
      ],
    'installable': True,
    'auto_install': False,
    'application': False,
}