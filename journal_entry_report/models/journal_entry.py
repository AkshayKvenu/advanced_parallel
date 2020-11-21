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

from odoo import models, fields, api, _
from time import time


class JournalReport(models.AbstractModel):
    _name = 'report.journal_entry_report.report_journal_entry'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'account.move'
        
        docs = self.env[model].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': self.env[model],
            'data': data,
            'docs': docs.sudo(),
            'time': time,
        }

    
class AccountInvoiceReport(models.AbstractModel):
    _name = "report.journal_entry_report.report_journal_entry_invoice"
    
    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'account.invoice' 
        active_ids = docids or self.env.context.get('active_id') or self.ids
        doc_ids = [x.move_id.id for x in self.env[model].browse(active_ids) if x.move_id] 
        
        model = 'account.move'
        docs = self.env[model].browse(doc_ids)

        return {
            'doc_ids': doc_ids,
            'doc_model': self.env[model],
            'data': data,
            'docs': docs.sudo(),
            'time': time,
        }
        

class PaymentVoucherReport(models.AbstractModel):
    _name = "report.journal_entry_report.report_journal_entry_voucher"
    
    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'account.voucher'
        active_ids = docids or self.env.context.get('active_id') or self.ids
        doc_ids = [x.move_id.id for x in self.env[model].browse(active_ids) if x.move_id] 
        
        model = 'account.move'
        docs = self.env[model].browse(doc_ids)

        return {
            'doc_ids': doc_ids,
            'doc_model': self.env[model],
            'data': data,
            'docs': docs.sudo(),
            'time': time,
        }

    
class PaymentReport(models.AbstractModel):
    _name = "report.journal_entry_report.report_journal_entry_payment"
     
    @api.model
    def _get_report_values(self, docids, data=None):
        model = 'account.payment' 
        active_ids = docids or self.env.context.get('active_id') or self.ids
        doc_lines = self.env['account.move.line'].search([('payment_id', '=', active_ids[0])])
        if doc_lines and doc_lines[0]:
            docs = doc_lines[0].move_id
        else:
            docs = self.env['account.move']
        
        model = 'account.move'

        return {
            'doc_ids': docs.ids,
            'doc_model': self.env[model],
            'data': data,
            'docs': docs.sudo(),
            'time': time,
            }

    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
