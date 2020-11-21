# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class WarningMesssage(models.TransientModel):
    _name = 'warning.message.wizard'
    
    name = fields.Text(string="Message",readonly=True,default="Tax is already duplicated")
 
    @api.multi
    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}
    
    
