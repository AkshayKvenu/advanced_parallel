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
    _name = 'report.account_excel_report.report_financial'
    _inherit = 'report.report_xlsx.abstract'
    
    
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet("Balance Sheet")
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
        
        
      
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        account_res = self.env['report.accounting_pdf_reports.report_financial'].with_context(data['form'].get('used_context',{})).get_account_lines(data.get('form'))
        
        if data['form']['account_report_id'][0] == 4:     
            sheet.merge_range('A3:H3', 'Balance Sheet', format1)
        elif data['form']['account_report_id'][0] == 1:
            sheet.merge_range('A3:H3', 'Profit and Loss', format1)
        sheet.merge_range('A4:H4', ' ')
        data=data['form']
        sheet.write(4, 1, 'Target Moves', format11)
        if data['target_move'] == 'all':
            sheet.write(5, 1, 'All Entries', format112)
        elif data['target_move'] == 'posted':
            sheet.write(5, 1, 'All Posted Entries', format112)
        if data['date_from']:
            sheet.write(4, 4, 'Date from', format11)
            sheet.write(4, 5, data['date_from'], format112)
        if data['date_to']:
            sheet.write(5, 4, 'Date to', format11)
            sheet.write(5, 5, data['date_to'], format112)
        
        report_model=self.env['report.accounting_pdf_reports.report_trialbalance']
        
        sheet.write(8, 1, 'name', format112)
        if data['debit_credit'] == 1:
            sheet.write(8, 4, 'Debit', format112)
            sheet.write(8, 5, 'Credit', format112)
        sheet.write(8, 6, 'Balance', format112)
        w_row_no = 9   
        for acc in account_res: 

            format=format112
            if acc['level'] == 1:
                format=format112
            elif acc['level'] == 4:
                format=format32
            if acc['level'] != 0:
                sheet.write(w_row_no, 1,acc['level']*' '+ acc['name'], format)
                
                if data['debit_credit'] == 1:
                    sheet.write(w_row_no, 4, acc['debit'], format)
                    sheet.write(w_row_no, 5, acc['credit'], format)
                sheet.write(w_row_no, 6, acc['balance'], format)
                w_row_no += 1   
                
                
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: