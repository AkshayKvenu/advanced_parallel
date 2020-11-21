{
    'name': 'Update Product Quantity on Hand Security',
    'version': '10.0',
    'license': 'LGPL-3',
    'author': 'Muhammad Faisal',
    'sequence': 1,
    'category': 'Warehouse',
    'website': 'http://Khatah.com',
    'summary' : 'Product on hand security',
    'description': '''
     This module will add a new security feature for the update product quantity on hand button in inventory module
    ''',
    'depends': ['stock','product'],
    'data': ['security/product_security_ext.xml','product_view_ext.xml'],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    "images":['static/description/banner.png'],

}
