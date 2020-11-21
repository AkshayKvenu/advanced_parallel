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
###############################################################################


from odoo import fields, models, _, api
from odoo.exceptions import UserError


class AccountReportFinancial(models.TransientModel):
    _inherit = "accounting.report" 

    account_analytic_id = fields.Many2many('account.analytic.account', string='Analytic Account')
    
    
    
    def _print_report(self, data):
        res = super(AccountReportFinancial, self)._print_report(data)
        res['data']['form'].update({'account_analytic_id': self.account_analytic_id.ids,'account_analytic_id_name':[rec.name for rec in self.account_analytic_id]})
        return res
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: