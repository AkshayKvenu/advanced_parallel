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

from odoo import models, fields, api, _
    
class Emailnotificationconfig(models.Model):
    _inherit = "res.company"
    
    email_notification_ids = fields.Many2many('res.users',string="Email notification when equipment is dispatched")
    
    
    @api.model
    def get_values(self):
        res = super(Emailnotificationconfig, self).get_values()
        field1 = self.env['ir.config_parameter'].sudo().get_param('advanced_lines_sale.email_notification_ids')
        print("ffffffffffffff",field1)
        res.update(
            {'email_notification_ids': field1,}
        )
        return res
 
    @api.multi
    def set_values(self):
        super(Emailnotificationconfig, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
 
        field1 = self.email_notification_ids and self.email_notification_ids.ids or False
        
        param.set_param('advanced_lines_sale.email_notification_ids', field1)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: