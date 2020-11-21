# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 Amzsys IT Solutions Pvt Ltd
#    (http://www.amzsys.com)
#    info@amzsys.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import datetime

from odoo import models, api, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.sipa_tax_report.report_tax_xlsx'
    _inherit = 'report.report_xlsx.abstract'
  
    def generate_xlsx_report(self, workbook, data, taxes):
        for obj in taxes:
            date_from = obj.date_from
            date_to = obj.date_to
            company_id = obj.company_id.id
            report_obj = self.env['report.sipa_tax_report.report_tax']
            lines = report_obj.get_lines(date_from, date_to, company_id)
            
            sheet = workbook.add_worksheet("Tax Report")
            format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center', 'bold': True})
            format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
            format21 = workbook.add_format({'font_size': 10, 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
            format22 = workbook.add_format({'font_size': 10, 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True, 'align': 'right', 'num_format': '#,###0.00'})
            format23 = workbook.add_format({'font_size': 10, 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True, 'align': 'center', 'num_format': '#,###0.00'})
            format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 10})
            format31 = workbook.add_format({'bottom': True, 'top': True, 'align': 'center', 'font_size': 10})
            format32 = workbook.add_format({'font_size': 10, 'right': True, 'left': True,'bottom': True, 'top': True, 'align': 'center', 'num_format': '#,###0.00'})
            format33 = workbook.add_format({'font_size': 10, 'right': True, 'left': True,'bottom': True, 'top': True, 'align': 'right', 'num_format': '#,###0.00'})
            
    #         font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
    #         red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8, 'bg_color': 'red'})         
    #         justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
    #         format3.set_align('center')
    #         font_size_8.set_align('center')
    #         justify.set_align('justify')
    #         format1.set_align('center')
    #         red_mark.set_align('center')
            sheet.merge_range('A3:I3', 'Tax Declaration', format1)
            sheet.merge_range('A4:I4', ' ')
            sheet.write(4, 0, 'From', format11)
            sheet.write(4, 1, str(datetime.datetime.strptime(str(date_from), '%Y-%m-%d').strftime('%d-%m-%Y')), format11)
            sheet.write(5, 0, 'To', format11)
            sheet.write(5, 1, str(datetime.datetime.strptime(str(date_to), '%Y-%m-%d').strftime('%d-%m-%Y')), format11)
            sheet.merge_range('A7:I7', ' ')
            
            w_row_no = 7
            
            # Purchase Details
            if lines['purchase']:
                sheet.merge_range(w_row_no, 0, w_row_no, 8, 'Purchase Details', format11)
                
                for line in lines['purchase'].values():
                    w_row_no += 1
                    sheet.merge_range(w_row_no, 0, w_row_no, 8, line[0][9], format21)
                    w_row_no += 1
                    sheet.write(w_row_no, 0, 'Journal No.', format11)
                    sheet.write(w_row_no, 1, 'Inv No', format11)
                    sheet.write(w_row_no, 2, 'Inv Date', format11)
                    sheet.write(w_row_no, 3, 'Partner', format11)
                    sheet.write(w_row_no, 4, 'VAT #', format11)
                    sheet.write(w_row_no, 5, 'VAT %', format11)
                    sheet.write(w_row_no, 6, 'Taxable Amt', format11)
                    sheet.write(w_row_no, 7, 'VAT Amount', format11)
                    sheet.write(w_row_no, 8, 'Total Amount', format11)
    
                    w_row_no += 1
                    for val in line:
                        sheet.write(w_row_no, 0, val[0], format3)
                        sheet.write(w_row_no, 1, val[1], format3)
                        sheet.write(w_row_no, 2, str(datetime.datetime.strptime(str(val[2]), '%Y-%m-%d').strftime('%d-%m-%Y')), format3)
                        sheet.write(w_row_no, 3, val[3], format3)
                        sheet.write(w_row_no, 4, val[4], format3)
                        sheet.write(w_row_no, 5, val[5], format32)
                        sheet.write(w_row_no, 6, val[6], format33)
                        sheet.write(w_row_no, 7, val[7], format33)
                        sheet.write(w_row_no, 8, val[6] + val[7], format33)
                        
                        w_row_no += 1
                        
                    sheet.merge_range(w_row_no, 0, w_row_no, 5, 'TOTAL', format21)
                    sheet.write(w_row_no, 6, sum(t[6] for t in line), format22)
                    sheet.write(w_row_no, 7, sum(t[7] for t in line), format22)
                    sheet.write(w_row_no, 8, sum(t[6] + t[7] for t in line), format22)
                
                w_row_no += 2
            
            # Sales Details
            if lines['sale']:
                sheet.merge_range(w_row_no, 0, w_row_no, 8, 'Sales Details', format11)
                
                for line in lines['sale'].values():
                    w_row_no += 1
                    sheet.merge_range(w_row_no, 0, w_row_no, 8, line[0][9], format21)
                    w_row_no += 1
                    sheet.write(w_row_no, 0, 'Journal No.', format11)
                    sheet.write(w_row_no, 1, 'Inv No', format11)
                    sheet.write(w_row_no, 2, 'Inv Date', format11)
                    sheet.write(w_row_no, 3, 'Partner', format11)
                    sheet.write(w_row_no, 4, 'VAT #', format11)
                    sheet.write(w_row_no, 5, 'VAT %', format11)
                    sheet.write(w_row_no, 6, 'Taxable Amt', format11)
                    sheet.write(w_row_no, 7, 'VAT Amount', format11)
                    sheet.write(w_row_no, 8, 'Total Amount', format11)
    
                    w_row_no += 1
                    for val in line:
                        sheet.write(w_row_no, 0, val[0], format3)
                        sheet.write(w_row_no, 1, val[1], format3)
                        sheet.write(w_row_no, 2, str(datetime.datetime.strptime(str(val[2]), '%Y-%m-%d').strftime('%d-%m-%Y')), format3)
                        sheet.write(w_row_no, 3, val[3], format3)
                        sheet.write(w_row_no, 4, val[4], format3)
                        sheet.write(w_row_no, 5, val[5], format32)
                        sheet.write(w_row_no, 6, val[6], format33)
                        sheet.write(w_row_no, 7, val[7], format33)
                        sheet.write(w_row_no, 8, val[6] + val[7], format33)
                        
                        w_row_no += 1
                        
                    sheet.merge_range(w_row_no, 0, w_row_no, 5, 'TOTAL', format21)
                    sheet.write(w_row_no, 6, sum(t[6] for t in line), format22)
                    sheet.write(w_row_no, 7, sum(t[7] for t in line), format22)
                    sheet.write(w_row_no, 8, sum(t[6] + t[7] for t in line), format22)
                
                w_row_no += 2
                
            # VAT Summary
            sheet.merge_range(w_row_no, 0, w_row_no, 3, 'VAT Summary', format11)
            w_row_no += 1
            for line in lines['all']:
                label = 'VAT at ' + str(line) + '%'
                sheet.merge_range(w_row_no, 0, w_row_no, 3, label, format21)
                w_row_no += 1
                sheet.write(w_row_no, 1, 'Sales', format11)
                sheet.write(w_row_no, 2, 'Purchase', format11)
                sheet.write(w_row_no, 3, 'Difference', format11)
                w_row_no += 1
                sale_amt = lines['all'][line]['sale'][0]
                pur_amt = lines['all'][line]['purchase'][0]
                sheet.write(w_row_no, 0, 'Taxable Amt', format3)
                sheet.write(w_row_no, 1, sale_amt, format33)
                sheet.write(w_row_no, 2, pur_amt, format33)
                sheet.write(w_row_no, 3, sale_amt - pur_amt, format33)
                w_row_no += 1
                sale_amt1 = lines['all'][line]['sale'][1]
                pur_amt1 = lines['all'][line]['purchase'][1]
                sheet.write(w_row_no, 0, 'Tax Amt', format3)
                sheet.write(w_row_no, 1, sale_amt1, format33)
                sheet.write(w_row_no, 2, pur_amt1, format33)
                sheet.write(w_row_no, 3, sale_amt1 - pur_amt1, format33)
                w_row_no += 1
                sale_amt2 = lines['all'][line]['sale'][2]
                pur_amt2 = lines['all'][line]['purchase'][2]
                sheet.write(w_row_no, 0, 'Total Amt', format3)
                sheet.write(w_row_no, 1, sale_amt2, format33)
                sheet.write(w_row_no, 2, pur_amt2, format33)
                sheet.write(w_row_no, 3, sale_amt2 - pur_amt2, format33)

            w_row_no += 2    
            
            # Tax Details
            sheet.merge_range(w_row_no, 0, w_row_no, 3, 'Tax Details', format11)
            w_row_no += 1
            sheet.write(w_row_no, 0, 'Tax Details', format11)
            sheet.write(w_row_no, 1, 'Taxable Amt', format11)
            sheet.write(w_row_no, 2, 'VAT Amount ', format11)
            sheet.write(w_row_no, 3, 'Total Amount', format11)
            w_row_no += 1
            if  lines['sale']:
                sheet.merge_range(w_row_no, 0, w_row_no, 3, 'Sales', format11)
                w_row_no += 1
                for line in lines['sale']:
                    label = lines['sale'][line][0][9]
                    sum_amt = sum(t[6] for t in lines['sale'][line])
                    sum_tax = sum(t[7] for t in lines['sale'][line])
                    sheet.write(w_row_no, 0, label, format3)
                    sheet.write(w_row_no, 1, sum_amt, format33)
                    sheet.write(w_row_no, 2, sum_tax, format33)
                    sheet.write(w_row_no, 3, sum_amt + sum_tax, format33)
                    w_row_no += 1
                
                tot_amt = sum(tl[6] for t in lines['sale'].values() for tl in t)
                tot_tax = sum(tl[7] for t in lines['sale'].values() for tl in t)
                sheet.write(w_row_no, 0, 'Total', format21)
                sheet.write(w_row_no, 1, tot_amt, format22)
                sheet.write(w_row_no, 2, tot_tax, format22)
                sheet.write(w_row_no, 3, tot_amt + tot_tax, format22)
                w_row_no += 1
                    
            if  lines['purchase']:
                sheet.merge_range(w_row_no, 0, w_row_no, 3, 'Purchase', format11)
                w_row_no += 1
                for line in lines['purchase']:
                    label = lines['purchase'][line][0][9]
                    sum_amt = sum(t[6] for t in lines['purchase'][line])
                    sum_tax = sum(t[7] for t in lines['purchase'][line])
                    sheet.write(w_row_no, 0, label, format3)
                    sheet.write(w_row_no, 1, sum_amt, format33)
                    sheet.write(w_row_no, 2, sum_tax, format33)
                    sheet.write(w_row_no, 3, sum_amt + sum_tax, format33)
                    w_row_no += 1
                
                tot_amt = sum(tl[6] for t in lines['purchase'].values() for tl in t)
                tot_tax = sum(tl[7] for t in lines['purchase'].values() for tl in t)
                sheet.write(w_row_no, 0, 'Total', format21)
                sheet.write(w_row_no, 1, tot_amt, format22)
                sheet.write(w_row_no, 2, tot_tax, format22)
                sheet.write(w_row_no, 3, tot_amt + tot_tax, format22)
                w_row_no += 1
            
            w_row_no += 1
            
            sheet.merge_range(w_row_no, 0, w_row_no, 2, 'Tax Difference', format11)
            w_row_no += 1
            sheet.write(w_row_no, 0, 'Sale', format11)
            sheet.write(w_row_no, 1, 'Purchase', format11)
            sheet.write(w_row_no, 2, 'Difference', format11)
            w_row_no += 1
            sum_sale = sum(tl[7] for t in lines['sale'].values() for tl in t)
            sum_pur = sum(tl[7] for t in lines['purchase'].values() for tl in t)
            sheet.write(w_row_no, 0, sum_sale, format23)
            sheet.write(w_row_no, 1, sum_pur, format23)
            sheet.write(w_row_no, 2, sum_sale - sum_pur, format23)
                
            
    
    @api.multi
    def get_lines(self, date_from, date_to):
#         query = """SELECT MIN(a.name), MAX(a.ref), m.date, MAX(p.name), MIN(p.vat), max(t.amount), m.tax_base_amount, ABS(COALESCE(SUM(m.debit-m.credit), 0)), MIN(a.amount), MIN(t.name) AS tax, MAX(j.type) AS type, MIN(t.id)
#                     FROM account_move_line AS m                                                                                                                                     
#                     INNER JOIN account_tax t ON (m.tax_line_id = t.id)           
#                     INNER JOIN account_move a ON (m.move_id = a.id)
#                     INNER JOIN account_journal j ON (m.journal_id = j.id)
#                     INNER JOIN res_partner p ON (m.partner_id = p.id)
#                     WHERE (a.date >= %s) AND (a.date <= %s) AND m.tax_exigible
#                     GROUP BY m.id;"""
 
        query = """SELECT a.name, a.ref, m.date, p.name, p.vat, t.amount, CASE WHEN COALESCE(SUM(m.debit-m.credit), 0) > 0.0 AND j.type = 'sale' THEN -1 *  m.tax_base_amount
                    WHEN COALESCE(SUM(m.debit-m.credit), 0) <  0.0 AND j.type = 'purchase' THEN -1 * m.tax_base_amount 
                    ELSE m.tax_base_amount END, 
                    CASE WHEN  j.type = 'sale' THEN -1 * COALESCE(SUM(m.debit-m.credit), 0) ELSE COALESCE(SUM(m.debit-m.credit), 0) END AS Tax, 
                    CASE WHEN COALESCE(SUM(m.debit-m.credit), 0) > 0.0 AND j.type = 'sale' THEN -1 * a.amount
                    WHEN COALESCE(SUM(m.debit-m.credit), 0) <  0.0 AND j.type = 'purchase'  THEN -1 * a.amount ELSE a.amount END AS Total, t.name AS tax, j.type AS type, t.id
                     
                    FROM account_move_line AS m
                    INNER JOIN account_tax t ON (m.tax_line_id = t.id)           
                    INNER JOIN account_move a ON (m.move_id = a.id)
                    INNER JOIN account_journal j ON (m.journal_id = j.id)
                    INNER JOIN res_partner p ON (m.partner_id = p.id)
                    WHERE (a.date >= %s) AND (a.date <= %s) AND m.tax_exigible
                    GROUP BY m.id, a.id, p.id, t.id, j.id 
                    ORDER BY m.date;"""
                     
        self.env.cr.execute(query, (date_from, date_to))
        results = self.env.cr.fetchall()
        
        print ("Res ; ", results)
         
        groups = dict((tp, {}) for tp in ['sale', 'purchase', 'all', 'general'])
        sale_groups = dict((tp[11], []) for tp in results if tp[10] == 'sale')
        pur_groups = dict((tp[11], []) for tp in results if tp[10] == 'purchase')
        gen_groups = dict((tp[11], []) for tp in results if tp[10] == 'general')
        groups['sale'] = sale_groups
        groups['purchase'] = pur_groups
        groups['general'] = gen_groups
         
        taxes = dict((t[5], {'sale': [0.0, 0.0, 0.0], 'purchase': [0.0, 0.0, 0.0], 'general': [0.0, 0.0, 0.0]}) for t in results)
 
        for line in results:
            print ("G ; ", [line[10]])
            print ("Gp ; ", groups[line[10]][line[11]])
            groups[line[10]][line[11]].append(line)
            print ("Line ; ", line)
            taxes[line[5]][line[10]][0] = sum([t[6] for t in results if t[5] == line[5] and t[10] == line[10]])
            taxes[line[5]][line[10]][1] = sum([t[7] for t in results if t[5] == line[5] and t[10] == line[10]])
            taxes[line[5]][line[10]][2] = sum([t[8] for t in results if t[5] == line[5] and t[10] == line[10]])
         
        groups['all'] = taxes
             
        print ("Grps ; ", groups)
        return groups
            


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
