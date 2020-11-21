# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class advanced_line_sale_mrp(models.Model):
#     _name = 'advanced_line_sale_mrp.advanced_line_sale_mrp'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100