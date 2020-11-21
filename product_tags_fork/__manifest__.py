# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Julius Network Solutions SARL <contact@julius.fr>
#    Copyright (C) 2015 credativ ltd. <info@credativ.co.uk>
#    Copyright (C) 2017-2018 Artem Shurshilov <shurshilov.a@yandex.ru>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

{
    "name": "Product Tags v. 12",
    "version": "1.0",
    'license': 'GPL-3',
    "author": "Shurshilov Artem",
#    "website": "https://vk.com/id20132180",
    'website': "http://www.eurodoo.com",
    "category": "Sales Management",
    "depends": [
        'product',
        'sale',
    ],
    "demo": [],
    "data": [
        'security/ir.model.access.csv',
        'product_view.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/kanban.png',
     ],
    'installable': True,
    'application': False,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
