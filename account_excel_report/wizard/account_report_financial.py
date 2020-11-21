# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) © 2019 KITE.
# (http://kite.com.sa)
# info@kite.com.sa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see .
#
##############################################################################

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class AccountReportGeneralLedger(models.TransientModel):
    _inherit = "accounting.report"

    @api.multi
    def export_xls(self):
        context = self._context
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read([])[0]
#         data['form'] = self.read(['account_report_id', 'date_from_cmp', 'date_to_cmp', 'journal_ids', 'filter_cmp', 'target_move','date_from', 'date_to', 'company_id','reconciled',"display_account",'enable_filter','debit_credit',"account_analytic_id"])[0]

        data['form']['comparison_context']  = self._build_comparison_context(data)     
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
        data['form'].update(self.read(['initial_balance', 'sortby'])[0])
        if data['form'].get('initial_balance') and not data['form'].get('date_from'):
            raise UserError(_("You must define a Start Date"))
        records = self.env[data['model']].browse(data.get('ids', []))
        
        data['form'].update({
                'model':self.env.context.get('active_model', 'ir.ui.menu'),
                'ids': self.env.context.get('active_ids', []),
            }) 
        
        if context.get('xls_export'):
            return self.env.ref('account_excel_report.account_report_financial_xlsx').report_action(self, data=data)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: