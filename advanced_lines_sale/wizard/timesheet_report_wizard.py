# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2016 Amzsys IT Solutions Pvt Ltd
# (http://www.amzsys.com)
# info@amzsys.com
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

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class TimesheetReportWizard(models.TransientModel):
    _name = "timesheet.report.wizard"
    _description = 'Timesheet Report Wizard'

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)


    @api.depends('start_date', 'end_date')
    def print_timesheet_report(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
                raise UserError(_("Start Date should be less than End Date."))
        
        context = self.env.context
        form = self.read()[0]
        start_date = form.get('start_date', False)
        end_date = form.get('end_date', False)
        date_list = []
        dt = start_date
        while dt <= end_date:
            date_list.append(dt)
            dt += timedelta(days = 1)

        timesheet_obj = self.env['project.task'].browse(context.get('active_ids')).mapped('timesheet_ids').filtered(
            lambda x: x.date >= start_date and x.date <= end_date)
        if not timesheet_obj:
            raise UserError(_("No data to print."))
        
        task_ids = self.env['project.task'].browse(context.get('active_ids'))
        timesheets = []
        for task in task_ids:
            task_dict = {'product': task.product_id.name, 'lot': task.lot_id.name}
            task_date_list = task.timesheet_ids.mapped('date')
            timesheet_date_list = []
            count = 0
            for dt in date_list:
                if dt in task_date_list:
                    timesheet_date_list.append('R')
                    count += 1
                else:
                    timesheet_date_list.append('NR')
            task_dict.update({'dates': timesheet_date_list, 'count': count})
            timesheets.append(task_dict)
        
        data = {'start_date': start_date, 'end_date': end_date, 'dates': date_list, 'timesheet': timesheets}
        return self.env.ref('advanced_lines_sale.report_task_timesheet').report_action(self, data=data)
        
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:  
