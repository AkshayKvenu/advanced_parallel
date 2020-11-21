# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2005-2006 Axelor SARL. (http://www.axelor.com)


from odoo import api, fields, models


class HolidaysRequest(models.Model):
    _inherit = "hr.leave"


    @api.multi
    def _create_resource_leave(self):
        """ This method will create entry in resource calendar leave object at the time of holidays validated """
        contract = self.env['hr.contract']
        for leave in self:
            date_from = fields.Datetime.from_string(leave.date_from)
            date_to = fields.Datetime.from_string(leave.date_to)
            
            contract_id = contract.search([('employee_id', '=', leave.employee_id.id), ('state', '=', 'open')], limit=1)

            vals = {
                    'name': leave.name,
                    'date_from': fields.Datetime.to_string(date_from),
                    'holiday_id': leave.id,
                    'date_to': fields.Datetime.to_string(date_to),
                    'resource_id': leave.employee_id.resource_id.id,
                    'time_type': leave.holiday_status_id.time_type,
                }
            if contract_id:
                vals.update({'calendar_id': contract_id.resource_calendar_id.id,})
            else:
                vals.update({'calendar_id': leave.employee_id.resource_calendar_id.id,})
            
            self.env['resource.calendar.leaves'].create(vals)
        return True

