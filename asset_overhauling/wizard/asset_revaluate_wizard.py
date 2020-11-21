# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AssetRevaluate(models.TransientModel):
    _name = 'asset.revaluate.wizard'
    
    def get_asset_object(self):
        return self.env['account.asset.asset'].browse(self.env.context.get('active_id'))
    
    def _compute_gross(self):
        return self.get_asset_object().value
        
    
    value = fields.Float("Gross Value", default=_compute_gross)
    
    def update_value(self):
        asset = self.get_asset_object()
        if asset.value != self.value:
            asset.value = self.value