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

import datetime 

from odoo import models, api, fields


class PartnerLedgerReportXls(models.AbstractModel):
    _name = 'report.account_excel_report.report_partner_ledger'
    _inherit = 'report.report_xlsx.abstract'
    
    
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Partner Ledger")
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format12 = workbook.add_format({'font_size': 12, 'align': 'left', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format111 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format112 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format113 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 10})
        format31 = workbook.add_format({'bottom': True, 'top': True, 'align': 'center', 'font_size': 10})
        format32 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True, 'bottom': True, 'top': True})
        format33 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': True, 'left': True, 'bottom': True, 'top': True})
        
        
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        data['computed'] = {}
        
        obj_partner = self.env['res.partner']
        query_get_data = self.env['account.move.line'].with_context(data['form'].get('used_context', {}))._query_get()
        data['computed']['move_state'] = ['draft', 'posted']
        if data['form'].get('target_move', 'all') == 'posted':
            data['computed']['move_state'] = ['posted']
        result_selection = data['form'].get('result_selection', 'customer')
        if result_selection == 'supplier':
            data['computed']['ACCOUNT_TYPE'] = ['payable']
        elif result_selection == 'customer':
            data['computed']['ACCOUNT_TYPE'] = ['receivable']
        else:
            data['computed']['ACCOUNT_TYPE'] = ['payable', 'receivable']
            
        partner_ledger_obj = self.env['report.accounting_pdf_reports.report_partnerledger']

        self.env.cr.execute("""
            SELECT a.id
            FROM account_account a
            WHERE a.internal_type IN %s
            AND NOT a.deprecated""", (tuple(data['computed']['ACCOUNT_TYPE']),))
        data['computed']['account_ids'] = [a for (a,) in self.env.cr.fetchall()]
        params = [tuple(data['computed']['move_state']), tuple(data['computed']['account_ids'])] + query_get_data[2]
        reconcile_clause = "" if data['form']['reconciled'] else ' AND "account_move_line".reconciled = false '
        query = """
            SELECT DISTINCT "account_move_line".partner_id
            FROM """ + query_get_data[0] + """, account_account AS account, account_move AS am
            WHERE "account_move_line".partner_id IS NOT NULL
                AND "account_move_line".account_id = account.id
                AND am.id = "account_move_line".move_id
                AND am.state IN %s
                AND "account_move_line".account_id IN %s
                AND NOT account.deprecated
                AND """ + query_get_data[1] + reconcile_clause
        self.env.cr.execute(query, tuple(params))
        partner_ids = [res['partner_id'] for res in self.env.cr.dictfetchall()]
        if data['form'].get('partner_ids',False):
            partner_ids = data['form'].get('partner_ids')
        partners = obj_partner.browse(partner_ids)
        partners = sorted(partners, key=lambda x: x.name)
        
        
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        init_balance = data['form'].get('initial_balance', True)
        sortby = data['form'].get('sortby', 'sort_date')
        codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]
        accounts = docs if self.model == 'account.account' else self.env['account.account'].search([])
            
        w_row_no = 9
        report_model=self.env['report.accounting_pdf_reports.report_partnerledger']
        for partner in partners:
            accounts_res = report_model.with_context(data['form'].get('used_context',{}))._lines( data, partner)
            data1 = data['form']
            
            sheet.merge_range('A3:H3', 'Partner Ledger', format1)
            sheet.merge_range('A4:H4', ' ')
            sheet.write(4, 0, 'Journals', format11)
            journals = ', '.join([ lt or '' for lt in codes ])
            sheet.write(5, 0, journals, format112)
            sheet.write(4, 6, 'Target Moves', format11)
            if data1['target_move'] == 'all':
                sheet.write(5, 6, 'All Entries', format112)
            elif data1['target_move'] == 'posted':
                sheet.write(5, 6, 'All Posted Entries', format112)
            if data1['date_from']:
                sheet.write(4, 3, 'Date from', format11)
                sheet.write(4, 4, data1['date_from'], format112)
            if data1['date_to']:
                sheet.write(5, 3, 'Date to', format11)
                sheet.write(5, 4, data1['date_to'], format112)
            
            sheet.write(8, 0, 'Date', format112)
            sheet.write(8, 1, 'JRNL', format112)
            sheet.write(8, 2, 'account', format112)
            sheet.write(8, 3, 'Ref', format112)
            sheet.write(8, 4, 'Debit', format112)
            sheet.write(8, 5, 'Credit', format112)
            sheet.write(8, 6, 'Balance', format112)
            sheet.merge_range(w_row_no, 0, w_row_no, 3, partner.name, format112)
            sheet.write( w_row_no, 4, str(report_model._sum_partner(data, partner, 'debit')), format112)
            sheet.write( w_row_no, 5, str(report_model._sum_partner(data, partner, 'credit')), format112)
            sheet.write( w_row_no, 6, str(report_model._sum_partner(data, partner, 'debit')-report_model._sum_partner(data, partner, 'credit')), format112)
            for acc in accounts_res:
                w_row_no += 1
                sheet.write(w_row_no, 0,  str(datetime.datetime.strptime(str(acc['date']), '%Y-%m-%d').strftime('%d-%m-%Y')), format32)
                sheet.write(w_row_no, 1, acc['code'], format32)
                sheet.write(w_row_no, 2, acc['a_code'], format32)
                sheet.write(w_row_no, 3, acc['displayed_name'], format32)
                sheet.write(w_row_no, 4, acc['debit'], format32)
                sheet.write(w_row_no, 5, acc['credit'], format32)
                sheet.write(w_row_no, 6, acc['progress'], format32)
            w_row_no += 1   



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: