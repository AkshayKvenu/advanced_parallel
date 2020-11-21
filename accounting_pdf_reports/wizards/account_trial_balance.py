# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountBalanceReport(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report'
    _description = 'Trial Balance Report'

    journal_ids = fields.Many2many('account.journal', 'account_balance_report_journal_rel', 'account_id', 'journal_id', string='Journals', required=True, default=[])
    account_analytic_ids = fields.Many2many('account.analytic.account', string='Analytic Account')

    def _print_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('accounting_pdf_reports.action_report_trial_balance').report_action(records, data=data)

    def pre_print_report(self, data):
        res = super(AccountBalanceReport, self).pre_print_report(data)
        res['form'] = self.read()[0] 
        return res
