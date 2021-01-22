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

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo import http
import re

class LeaveRejection(models.TransientModel):
    _name = 'leave.rejection'
    
    rejection_reason = fields.Text(string="Rejection reason", required=True)
    
    
    @api.multi
    def submit_method(self):
        leave_obj = self.env['hr.leave']
        hr_leave = leave_obj.browse(self._context.get('active_ids'))[0]
        if not hr_leave:
            return True
        if any(holiday.state not in ['confirm', 'validate', 'validate1','hr_approval'] for holiday in hr_leave):
            raise UserError(_('Leave request must be confirmed or validated in order to refuse it.'))
        
        # Delete the meeting
        hr_leave.mapped('meeting_id').unlink()
        # If a category that created several holidays, cancel all related
        linked_requests = hr_leave.mapped('linked_request_ids')
        if linked_requests:
            linked_requests.action_refuse()
        hr_leave._remove_resource_leave()
        hr_leave.activity_update()
        
        for line in self:
            hr_leave.rejection_reason = line.rejection_reason
            hr_leave.write({'state': 'refuse'})
            for holiday in hr_leave:
                action = self.env.ref('hr_holidays.hr_leave_action_all', False)
                base_url = http.request.httprequest.referrer
                base_url = re.sub('\?.*', '', base_url)
                base_url += '#id=%s&action=%s&model=hr.leave&view_type=form' % (hr_leave.id, action.id)
                
                rejectn = holiday.rejection_reason
                template = self.env.ref('hr_holidays_multi_levels_approval.hr_leave_rejection_email_template', False)
                template.with_context(url=base_url,rejectns=rejectn).send_mail(hr_leave.id, force_send=True)
        return True
    
#     @api.multi
#     def action_refuse(self):
#         current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
# #         if any(holiday.state not in ['confirm', 'validate', 'validate1'] for holiday in self):
# #             raise UserError(_('Leave request must be confirmed or validated in order to refuse it.'))
# 
#         validated_holidays = self.filtered(lambda hol: hol.state == 'validate1')
#         validated_holidays.write({'state': 'refuse', 'first_approver_id': current_employee.id})
#         (self - validated_holidays).write({'state': 'refuse', 'second_approver_id': current_employee.id})
#         # Delete the meeting
#         self.mapped('meeting_id').unlink()
#         # If a category that created several holidays, cancel all related
#         linked_requests = self.mapped('linked_request_ids')
#         if linked_requests:
#             linked_requests.action_refuse()
#         self._remove_resource_leave()
#         self.activity_update()
#         return True
