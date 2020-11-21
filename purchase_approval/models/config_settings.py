# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    mail_send_to = fields.Many2many('res.users',related='company_id.mail_send_to',readonly=False)
    approved_mail_send_to = fields.Many2many('res.users',related='company_id.approved_mail_send_to',readonly=False)
      
    
    @api.multi
    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('purchase_approval.mail_send_to', self.mail_send_to.ids)
        self.env['ir.config_parameter'].sudo().set_param('purchase_approval.approved_mail_send_to', self.approved_mail_send_to.ids)
        return res
      
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        mail_send_to = self.env['ir.config_parameter'].sudo().get_param('purchase_approval.mail_send_to')
        approved_mail_send_to = self.env['ir.config_parameter'].sudo().get_param('purchase_approval.approved_mail_send_to')
          
        if mail_send_to == False:
            res.update(
            mail_send_to=[(6, 0, literal_eval('None'))],
            )
              
        else:
            res.update(
            mail_send_to=[(6, 0, literal_eval(mail_send_to))],
            )
          
        if approved_mail_send_to == False:
            res.update(
            approved_mail_send_to=[(6, 0, literal_eval('None'))],
            )
               
        else:
            res.update(
            approved_mail_send_to=[(6, 0, literal_eval(approved_mail_send_to))],
            )
        return res
    
        
