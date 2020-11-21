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


class GeneralLedgerReportXls(models.AbstractModel):
    _name = 'report.account_excel_report.report_general_ledger'
    _inherit = 'report.report_xlsx.abstract'
    

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Genaral Ledger")
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
        
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        model = data['form'].get('model', False)
        active_ids = data['form']['ids']
        docs = self.env[model].browse(active_ids)

        init_balance = data['form'].get('initial_balance', True)
        sortby = data['form'].get('sortby', 'sort_date')
        display_account = data['form']['display_account']
        codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]

        accounts = docs if data['model'] == 'account.account' else self.env['account.account'].search([])
        accounts_res = self.env['report.accounting_pdf_reports.report_generalledger'].with_context(data['form'].get('used_context',{}))._get_account_move_entry(accounts, init_balance, sortby, display_account)
        data = data['form']
        
        sheet.merge_range('A3:H3', 'General Ledger', format1)
        sheet.merge_range('A4:H4', ' ')
        sheet.write(4, 0, 'Journals', format11)
        journals = ', '.join([ lt or '' for lt in codes ])
        sheet.write(5, 0, journals, format112)
        sheet.write(4, 3, 'Display Account', format11)
        if data['display_account'] == 'all':
            sheet.write(5, 3, 'All accounts', format112)
        elif data['display_account'] == 'movement':
            sheet.write(5, 3, 'With movements', format112)
        elif data['display_account'] == 'not_zero':
            sheet.write(5, 3, 'With balance not equal to zero', format112)
        sheet.write(4, 6, 'Target Moves', format11)
        if data['target_move'] == 'all':
            sheet.write(5, 6, 'All Entries', format112)
        elif data['target_move'] == 'posted':
            sheet.write(5, 6, 'All Posted Entries', format112)
        sheet.write(6, 0, 'Sorted By', format11)
        if data['sortby'] == 'sort_date':
            sheet.write(6, 1, 'Date', format112)
        elif data['sortby'] == 'sort_journal_partner':
            sheet.write(6, 1, 'Journal and Partner', format112)
        if data['date_from']:
            sheet.write(6, 3, 'Date from', format11)
            sheet.write(6, 4, data['date_from'], format112)
        if data['date_to']:
            sheet.write(6, 6, 'Date to', format11)
            sheet.write(6, 7, data['date_to'], format112)
        
        w_row_no = 8
        
        sheet.write(w_row_no, 0, 'Date', format112)
        sheet.write(w_row_no, 1, 'JRNL', format112)
        sheet.write(w_row_no, 2, 'Partner', format112)
        sheet.write(w_row_no, 3, 'Ref', format112)
        sheet.write(w_row_no, 4, 'Move', format112)
        sheet.write(w_row_no, 5, 'Entry Label', format112)
        sheet.write(w_row_no, 6, 'Debit', format112)
        sheet.write(w_row_no, 7, 'Credit', format112)
        sheet.write(w_row_no, 8, 'Balance', format112)
        
        for acc in accounts_res:
            w_row_no += 1
            acc_name = '  ' + acc['code'] + acc['name']
            sheet.merge_range(w_row_no, 0, w_row_no, 5, acc_name, format112)
            sheet.write(w_row_no, 6, acc['debit'], format113)
            sheet.write(w_row_no, 7, acc['credit'], format113)
            sheet.write(w_row_no, 8, acc['balance'], format113)
            
            for line in acc['move_lines']:
                w_row_no += 1
                sheet.write(w_row_no, 0, line['ldate'], format31)
                sheet.write(w_row_no, 1, line['lcode'], format31)
                sheet.write(w_row_no, 2, line['partner_name'], format32)
                sheet.write(w_row_no, 3, line['lref'], format32)
                sheet.write(w_row_no, 4, line['move_name'], format32)
                sheet.write(w_row_no, 5, line['lname'], format32)
                sheet.write(w_row_no, 6, line['debit'], format33)
                sheet.write(w_row_no, 7, line['credit'], format33)
                sheet.write(w_row_no, 8, line['balance'],format33 )
                



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: