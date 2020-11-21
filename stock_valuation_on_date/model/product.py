# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)
#
#################################################################################

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    is_an_asset = fields.Boolean(string='Is An Asset?',default=False)
    
    type = fields.Selection([('consu', 'Deliverable Service'), ('service', 'Service'), ('product', 'Storable Product')],string='Product Type', default = 'consu')
   
    @api.onchange('type')
    def change_type(self):
        for vals in self:
            if vals.type=='consu' or vals.type=='service':
                vals.is_an_asset = False
                
                
    
