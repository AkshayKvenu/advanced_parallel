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

from odoo import models, fields, api
    
class UomUom(models.Model):
    _inherit = "uom.uom"

    period_type = fields.Selection([('day', 'Day'), ('month', 'Month')], 'Period Type')
    is_day = fields.Boolean('Is Day')
    is_month = fields.Boolean('Is Month')
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: