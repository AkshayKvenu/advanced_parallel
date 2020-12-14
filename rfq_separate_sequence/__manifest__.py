# -*- encoding: utf-8 -*-
{
    'name' : 'SW - RFQ Separate Sequence',
    'version' : '12.0.1.3',
    'category' : 'Purchase',
    'author' : 'Smart Way Business Solutions',
    'website' : 'https://www.smartway.co',
    'license':  "Other proprietary",
    'summary': """Add a special sequence to your RFQs""",
    'data': ['sequence.xml'],
    'depends' : ['base', 'purchase','stock','purchase_approval'],
    'images':  ["static/description/image.png"],
    'installable': True,
    'auto_install': False,
}