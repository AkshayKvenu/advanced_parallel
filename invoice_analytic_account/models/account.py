# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    account_analytic_id = fields.Many2one('account.analytic.account')


    def set_analytic_lines(self):
        for line in self.invoice_line_ids:
            line.account_analytic_id = self.account_analytic_id
    

            