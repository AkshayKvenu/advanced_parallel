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
    _name = 'report.account_excel_report.report_trialbalance'
    _inherit = 'report.report_xlsx.abstract'
    
    
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Partner Ledger")
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format12 = workbook.add_format({'font_size': 12, 'align': 'left', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format111 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format112 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format113 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True, 'num_format': '#,##0.00'})
        format21 = workbook.add_format({'font_size': 10, 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 10})
        format31 = workbook.add_format({'bottom': True, 'top': True, 'align': 'center', 'font_size': 10})
        format32 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': True, 'left': True, 'bottom': True, 'top': True})
        format33 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': True, 'left': True, 'bottom': True, 'top': True, 'num_format': '#,##0.00'})


        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        data=data['form']
        target_move = data.get('target_move')
        display_account = data.get('display_account')
        accounts = docs if self.model == 'account.account' else self.sudo().env['account.account'].search([('company_id', '=', data['company_id'][0])])
        account_res = self.env['report.accounting_pdf_reports.report_trialbalance'].with_context(data)._get_accounts(accounts, display_account, target_move)
        
        sheet.merge_range('A3:F3', 'Trial Balance', format1)
        sheet.merge_range('A4:F4', ' ')
        sheet.write(4, 0, 'Display Account', format112)
        if data['display_account'] == 'all':
            sheet.write(5, 0, 'All accounts', format112)
        elif data['display_account'] == 'movement':
            sheet.write(5, 0, 'With movements', format112)
        elif data['display_account'] == 'not_zero':
            sheet.write(5, 0, 'With balance not equal to zero', format112)
        sheet.write(4, 5, 'Target Moves', format112)
        if data['target_move'] == 'all':
            sheet.write(5, 5, 'All Entries', format112)
        elif data['target_move'] == 'posted':
            sheet.write(5, 5, 'All Posted Entries', format112)
        if data['date_from']:
            sheet.write(4, 2, 'Date from', format112)
            sheet.write(4, 3, data['date_from'], format112)
        if data['date_to']:
            sheet.write(5, 2, 'Date to', format112)
            sheet.write(5, 3, data['date_to'], format112)
        
        
        sheet.write(8, 0, 'Code', format112)
        sheet.write(8, 1, 'account', format112)
        sheet.write(8, 2, 'Initial Balance', format112)
        sheet.write(8, 3, 'Debit', format112)
        sheet.write(8, 4, 'Credit', format112)
        sheet.write(8, 5, 'Balance', format112)
        w_row_no = 9       
        
        if account_res:
            for key in account_res:
                w_row_no += 1
                if key == None :
                    sheet.merge_range(w_row_no , 0, w_row_no, 1, 'Undefined', format112)
                else:
                    sheet.merge_range(w_row_no , 0, w_row_no, 1, account_res[key][0]['analytic_name'], format112)
                initial = 0
                debit = 0
                credit = 0
                balance = 0
                for acc in account_res[key]:
                    initial += acc['initial']
                    debit += acc['debit']
                    credit += acc['credit']
                    balance += acc['debit'] - acc['credit'] + acc['initial']
                sheet.write(w_row_no , 2, initial , format113)
                sheet.write(w_row_no , 3, debit , format113)
                sheet.write(w_row_no , 4, credit , format113)
                sheet.write(w_row_no , 5, balance , format113)
                
                for acc in account_res[key]:
                    w_row_no += 1
                    sheet.write(w_row_no, 0, acc['code'], format32)
                    sheet.write(w_row_no, 1, acc['name'], format32)
                    sheet.write(w_row_no, 2, acc['initial'], format33)
                    sheet.write(w_row_no, 3, acc['debit'], format33)
                    sheet.write(w_row_no, 4, acc['credit'], format33)
                    sheet.write(w_row_no, 5, acc['debit'] - acc['credit'] + acc['initial'], format33)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: