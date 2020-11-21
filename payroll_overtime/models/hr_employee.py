# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Hr_Employee(models.Model):
     
    _inherit = 'hr.employee'   
    
    
    @api.multi
    @api.depends('name', 'barcode')
    def name_get(self):
        result = []
        for rec in self:
            name = str(rec.name) + ' ' +'[' + str(rec.barcode) +']'
            result.append((rec.id, name))
        return result
    
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            args = ['|', ('name', operator, name), ('barcode', operator, name)] + args
        tags = self.search(args, limit=limit)
        return tags.name_get()
  