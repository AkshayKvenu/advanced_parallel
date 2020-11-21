from odoo import fields, models, api


class Account(models.Model):
    
    _inherit = "account.account"
    
    manual_entry = fields.Boolean("Do Not Allow Manual Entries")