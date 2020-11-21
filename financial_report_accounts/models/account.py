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


class Account(models.Model):
    _inherit = 'account.account'
    
    financial_report_ids = fields.Many2many('account.financial.report', 'account_financial_report_rel', 'account_id', 'financial_report_id',\
                                             string="Financial Reports", compute="_get_financial_reports")
    
    
    @api.one
    def _get_financial_reports(self):
        report_obj = self.env['account.financial.report']
        account_reports = report_obj.search([('type', '=', 'accounts')])
        account_type_reports = report_obj.search([('type', '=', 'account_type')])
        
        account_ids = [r.id for r in account_reports if r.account_ids and self.id in r.account_ids.ids]
        
        type_account_ids = [r.id for r in account_type_reports if r.account_type_ids and self.user_type_id.id in r.account_type_ids.ids]
        
        self.financial_report_ids = [(6, 0, account_ids + type_account_ids)]
    
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
