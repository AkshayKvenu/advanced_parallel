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
from num2words import num2words
import math

class PurchaseOrder(models.Model):
    _inherit='purchase.order'


    ikvta = fields.Float(string="IKVTA %" ,readonly=True)
    Updated_date = fields.Date(string="Updated Date" ,readonly=True)
    mode_of_shipment = fields.Many2one("purchase.mode.of.shipment")
    
        
    @api.one
    @api.depends('amount_total')
    def _compute_amount_words(self):
        lang = self.env.user.lang
#         number_dec = 0
        number_dec = str(self.amount_total).split('.')[1]
        print('nnnmmm',self.amount_total)
        numb = int(number_dec[0])
        numb1 = int(number_dec[1]) if len(number_dec) > 1 else 0
        number_dec = int(number_dec)
        self.amount_words = (num2words(math.floor(self.amount_total), lang=lang) +"  "+ self.currency_id.currency_unit_label).title()
        
        if number_dec > 0:
            if numb!=0 and numb1 == 0:
                number_dec *= 10
            self.amount_words += "  and  " + (num2words(math.floor(number_dec), lang=lang) +"  "+ self.currency_id.currency_subunit_label).title()
    
    amount_words = fields.Char(string='Total in words:',compute='_compute_amount_words')
    
    @api.onchange('partner_id')
    def partnerchange(self):
        if self.partner_id.supplier:
            self.ikvta=self.partner_id.ikvta
            self.Updated_date=self.partner_id.Updated_date
        
        
    @api.model
    def create(self,vals):
        line = super(PurchaseOrder, self).create(vals)
        line.ikvta=line.partner_id.ikvta
        line.Updated_date=line.partner_id.Updated_date
        return line
    
    
    @api.multi
    def write(self, vals):
        if 'partner_id' in vals and vals['partner_id']:
            partner_obj = self.env['res.partner'].browse(vals['partner_id'])
            vals['ikvta'] = partner_obj.ikvta
            vals['Updated_date'] = partner_obj.Updated_date
        res=super(PurchaseOrder, self).write(vals)
        return res
    
class PurchaseOrderShipment(models.Model):
    _name='purchase.mode.of.shipment'
    name = fields.Char("Name")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: