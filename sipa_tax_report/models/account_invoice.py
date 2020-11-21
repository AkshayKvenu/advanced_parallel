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


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'    
    
    @api.model
    def tax_line_move_line_get(self):
        res = []
        # keep track of taxes already processed
        done_taxes = []
        print ("\n ", done_taxes)
        # loop the invoice.tax.line in reversal sequence
        for tax_line in sorted(self.tax_line_ids, key=lambda x: -x.sequence):
#             if tax_line.amount_total:
            tax = tax_line.tax_id
            if tax.amount_type == "group":
                for child_tax in tax.children_tax_ids:
                    done_taxes.append(child_tax.id)
            res.append({
                'invoice_tax_line_id': tax_line.id,
                'tax_line_id': tax_line.tax_id.id,
                'type': 'tax',
                'name': tax_line.name,
                'price_unit': tax_line.amount_total,
                'quantity': 1,
                'price': tax_line.amount_total,
                'account_id': tax_line.account_id.id,
                'account_analytic_id': tax_line.account_analytic_id.id,
                'invoice_id': self.id,
                'tax_ids': [(6, 0, list(done_taxes))] if tax_line.tax_id.include_base_amount else []
            })
            done_taxes.append(tax.id)
        return res
    

    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
