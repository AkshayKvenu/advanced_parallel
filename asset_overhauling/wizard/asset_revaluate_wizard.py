# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AssetRevaluate(models.TransientModel):
    _name = 'asset.revaluate.wizard'
    
    def get_asset_object(self):
        return self.env['account.asset.asset'].browse(self.env.context.get('active_id'))
    
    def _compute_gross(self):
        return self.get_asset_object().value
    
    def _compute_temp(self):
        move_value = 0.0
        for rec in self.temp_move_line_ids:
            move_value += rec.debit
        return self.get_asset_object().value - move_value
    
#     def _compute_move_line(self):
#         res = self.env['account.move.line'].search([('asset_id', '=', self.get_asset_object().id)])
#         move_ids = res.mapped('id')
#         return [(6,0,move_ids)]
    
    def _compute_move_line_temp(self):
        res = self.env['account.move.line'].search([('asset_id', '=', self.get_asset_object().id)])
        move_ids = res.mapped('id')
        return [(6,0,move_ids)]
        
    
    value = fields.Float("Gross Value", default=_compute_gross)
    value_tmp = fields.Float("Temp Value", default=_compute_temp)
    move_line_ids = fields.Many2many('account.move.line', string="Move lines")
    temp_move_line_ids = fields.Many2many('account.move.line', default=_compute_move_line_temp, string="Move lines")
    
#     @api.onchange('move_line_ids')
#     def compute_value_onchange(self):
#         value = self.value_tmp
#         for val in self.move_line_ids:
#             value += val.debit
#         self.value = value
    
    @api.onchange('move_line_ids')
    def compute_value_onchange(self):
        value = self._compute_gross()
        for val in self.move_line_ids:
            value += val.debit
        self.value = value
    
    def update_value(self):
        value = self._compute_gross()
        print("bbbbbbbbbbb",value)
#         for val in self.temp_move_line_ids:
#             val.asset_id = False
        asset = self.get_asset_object()
        for line in self.move_line_ids:
            print("cccccccccccc",line.debit)
            value += line.debit
            line.asset_id = asset.id
        print("aaaaaaaaaaaaaa",value)
#         print("aaaaaaaaaaaaaa",value1)
        if asset.value != value:
            asset.value = value
            
            
            
            
            
            
            
            