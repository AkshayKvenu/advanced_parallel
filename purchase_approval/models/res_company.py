# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    mail_send_to = fields.Many2many('res.users', 'res_user_mail_res_user_rel', 'user_id', 'mail_user_id')
    approved_mail_send_to = fields.Many2many('res.users', 'res_user_approve_mail_res_user_rel', 'user_id', 'mail_user_id')
    
