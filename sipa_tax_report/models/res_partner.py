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

from openerp import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'
    
    
    
    @api.multi
    def write(self, vals):
        vat = vals['vat'] if 'vat' in vals else self.vat or False
        if vat:
            if not len(vat) == 15:
                raise ValidationError(_("Please enter a valid VAT.\nVAT should contain 15 characters."))
        return super(Partner, self).write(vals)

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
