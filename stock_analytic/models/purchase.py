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


from odoo import api, fields, models


class Stock_purchase_analytic(models.Model):
    _inherit = "purchase.order.line"
      
      
    @api.multi  
    def _prepare_stock_moves(self, picking):
        res = super(Stock_purchase_analytic, self)._prepare_stock_moves(picking)      
        res[0]['analytic_account_id']=self.account_analytic_id.id
        return res
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: