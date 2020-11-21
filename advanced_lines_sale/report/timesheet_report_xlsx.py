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

from odoo import models
from datetime import date, datetime, timedelta


class TimesheetXlsx(models.AbstractModel):
    _name = 'report.advanced_lines_sale.task_timesheet_report.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, tasks):
        start_date = datetime.strptime(data.get('start_date', False), '%Y-%m-%d')
        end_date = datetime.strptime(data.get('end_date', False), '%Y-%m-%d')
        
        report_name = 'Timesheet from ' + str(start_date)[:10] + ' to ' + str(end_date)[:10]
        sheet = workbook.add_worksheet('Timesheet')
        format1 = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14, 'bg_color': '#8bc6e9'})
        format2 = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 12, 'bg_color': '#b5b3d9'})
        format21 = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 12, 'rotation': 90, 'bg_color': '#b5b3d9'})
        format22 = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 12, 'bg_color': '#5cc942'})
        format23 = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 12, 'bg_color': '#f15e57'})
        format3 = workbook.add_format({'align': 'left', 'font_size': 12})
        format31 = workbook.add_format({'align': 'center', 'font_size': 12})
        format32 = workbook.add_format({'align': 'center', 'font_size': 12, 'bg_color': 'green'})
        format33 = workbook.add_format({'align': 'center', 'font_size': 12, 'bg_color': 'red'})
        
        sheet.set_row(0, 20)
        sheet.merge_range(0, 0, 0, len(data.get('dates')) + 2, report_name, format1)
        
        sheet.set_row(1, 80)
        sheet.set_column(1, 1, 10)
        sheet.set_column(2, len(data.get('dates')) + 1, 5)
        sheet.write(1, 0, 'Product', format2)
        sheet.write(1, 1, 'Serial No.', format2)
        column = 2
        for dt in data.get('dates'):
            sheet.write(1, column, str(dt), format21)
            column += 1
        sheet.write(1, column, 'Total', format2)
        
        row = 2
        
        for line in data.get('timesheet'):
            sheet.write(row, 0, line['product'])
            sheet.write(row, 1, line['lot'])
            column = 2
            for dt in line['dates']:
                if dt == 'R':
                    sheet.write(row, column, dt, format32)
                else:
                    sheet.write(row, column, dt, format33)
                column += 1
            sheet.write(row, column, line['count'], format31)
            row += 1
            
        row += 3
        sheet.write(row, 1, 'R', format22)
        sheet.merge_range(row, 2, row, 4, 'Rented', format22)
        row += 1
        sheet.write(row, 1, 'NR', format23)
        sheet.merge_range(row, 2, row, 4, 'Not Rented', format23)
            


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: