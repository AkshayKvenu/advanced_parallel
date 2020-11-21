# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.multi
    def set_values(self):
        """Set values for configuration"""
        super(ResConfigSettings, self).set_values()
        Param = self.env['ir.config_parameter'].sudo()
        Param.set_param('stock.group_stock_production_lot', self.group_stock_production_lot)

    @api.multi
    def get_values(self):
        """Get values for configuration"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(group_stock_production_lot=params.get_param('stock.group_stock_production_lot'))
        return res