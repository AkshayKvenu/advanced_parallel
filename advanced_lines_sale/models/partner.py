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
from _datetime import date


class ResPartner(models.Model):
    _inherit='res.partner'
     
    cr_number = fields.Char(string="CR Number")
    ikvta = fields.Float(string="IKVTA %")
    Updated_date=fields.Date(string="Updated Date",default=date.today())


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

