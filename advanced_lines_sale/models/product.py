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

import re 

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import ValidationError, RedirectWarning, UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    def _get_default_category_id(self):
        if self._context.get('categ_id') or self._context.get('default_categ_id'):
            return self._context.get('categ_id') or self._context.get('default_categ_id')
        category = self.env.ref('product.product_category_all', raise_if_not_found=False)
        if not category:
            category = self.env['product.category'].search([], limit=1)
        if category:
            return category.id
        else:
            err_msg = _('You must define at least one product category in order to be able to create products.')
            redir_msg = _('Go to Internal Categories')
            raise RedirectWarning(err_msg, self.env.ref('product.product_category_action_form').id, redir_msg)

    categ_id = fields.Many2one('product.category', 'Product Category', default=_get_default_category_id,
        change_default=True, track_visibility='onchange',
        required=True, help="Select category for the current product")
    
    is_rental = fields.Boolean('Rental Equipment')
    rental_uom_id = fields.Many2one('uom.uom', 'Rental Unit of Measure', help="Default unit of measure used for rental operations.", domain="[('period_type', '!=', False)]")
    secondary_rental_uom_id = fields.Many2one('uom.uom', 'Secondary Rental Unit of Measure', help="Default unit of measure used for rental operations.", domain="[('period_type', '!=', False)]")
    
    @api.constrains('default_code')
    def _check_internal_ref(self):
        if self.default_code:
            partner_rec = self.search([('default_code','=', self.default_code),('id','!=',self.id)])
            if partner_rec:
                raise ValueError(_('Exists ! Internal reference must be unique!'))
    
    @api.onchange('is_rental')
    def _set_rental_product(self):
        if self.is_rental:
            self.update({
                    'type': 'product',
                    'tracking': 'serial',
                    'invoice_policy': 'delivery',
                    'service_policy': 'delivered_timesheet',
                })
            
            
class Product(models.Model):
    _inherit = 'product.product'
    
    
    @api.onchange('is_rental')
    def _set_rental_product(self):
        if self.is_rental:
            self.update({
                    'type': 'product',
                    'tracking': 'serial',
                    'invoice_policy': 'delivery',
                    'service_policy': 'delivered_timesheet',
                })
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        product_ids =[]
        line = super(Product, self)._name_search(name,args,operator,limit,name_get_uid)
        product_ids = self._search([('description_purchase', operator, name)] + args, limit=limit, access_rights_uid=name_get_uid)
        products = self.browse(product_ids).name_get() 
        print("bbbbbbbbbbbbbbbbbbbbbb",products) 
        for prod in products:
            line.append(prod)   
        print("aaaaaaaaaaaaaaaaaaaaaaa",line)
        return line
        
        



#     @api.model
#     def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
#         if not args:
#             args = []
#         if name:
#             positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
#             product_ids = []
#             if operator in positive_operators:
#                 product_ids = self._search([('default_code', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
#                 if not product_ids:
#                     product_ids = self._search([('barcode', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
#                 if not product_ids:
#                     product_ids = self._search([('description_purchase', operator, name)] + args, limit=limit, access_rights_uid=name_get_uid)
#             if not product_ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
#                 # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
#                 # on a database with thousands of matching products, due to the huge merge+unique needed for the
#                 # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
#                 # Performing a quick memory merge of ids in Python will give much better performance
#                 product_ids = self._search(args + [('default_code', operator, name)], limit=limit)
#                 if not limit or len(product_ids) < limit:
#                     # we may underrun the limit because of dupes in the results, that's fine
#                     limit2 = (limit - len(product_ids)) if limit else False
#                     product2_ids = self._search(args + [('name', operator, name), ('id', 'not in', product_ids)], limit=limit2, access_rights_uid=name_get_uid)
#                     product_ids.extend(product2_ids)
#             elif not product_ids and operator in expression.NEGATIVE_TERM_OPERATORS:
#                 domain = expression.OR([
#                     ['&', ('default_code', operator, name), ('name', operator, name)],
#                     ['&', ('default_code', '=', False), ('name', operator, name)],
#                 ])
#                 domain = expression.AND([args, domain])
#                 product_ids = self._search(domain, limit=limit, access_rights_uid=name_get_uid)
#             if not product_ids and operator in positive_operators:
#                 ptrn = re.compile('(\[(.*?)\])')
#                 res = ptrn.search(name)
#                 if res:
#                     product_ids = self._search([('default_code', '=', res.group(2))] + args, limit=limit, access_rights_uid=name_get_uid)
#             # still no results, partner in context: search on supplier info as last hope to find something
#             if not product_ids and self._context.get('partner_id'):
#                 suppliers_ids = self.env['product.supplierinfo']._search([
#                     ('name', '=', self._context.get('partner_id')),
#                     '|',
#                     ('product_code', operator, name),
#                     ('product_name', operator, name)], access_rights_uid=name_get_uid)
#                 if suppliers_ids:
#                     product_ids = self._search([('product_tmpl_id.seller_ids', 'in', suppliers_ids)], limit=limit, access_rights_uid=name_get_uid)
#         else:
#             product_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
#         return self.browse(product_ids).name_get()


    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: