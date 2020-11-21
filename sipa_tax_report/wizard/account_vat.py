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

# class AccountVat(models.TransientModel):
#     _inherit = "account.common.partner.report"
#     _name = 'account.vat'
#     _description = "Account VAT"
#     
#     target_vat = fields.Selection([('out_invoice', 'Sales VAT'), ('in_invoice', 'Purchase VAT')], string="Target VAT", default='out_invoice')
# 
#     def _print_report(self, data):
#         data = self.pre_print_report(data)
#         return self.env['report'].get_action(self, 'account_vat_report.report_vat_range', data=data)
#     
#     @api.multi
#     def pre_print_report(self, data):
#         data = super(AccountVat, self).pre_print_report(data)
#         data['form'].update(self.read(['target_vat'])[0])
#         return data
#     
#     @api.multi
#     def export_xls(self):
#         context = self._context
#         datas = {'ids': context.get('active_ids', [])}
#         datas['model'] = 'account.invoice'
#         datas['form'] = self.read()[0]
#         for field in datas['form'].keys():
#             if isinstance(datas['form'][field], tuple):
#                 datas['form'][field] = datas['form'][field][0]
#         if context.get('xls_export'):
#             return {'type': 'ir.actions.report.xml',
#                     'report_name': 'account_vat_report.vat_report_xls.xlsx',
#                     'datas': datas,
#                     'name': 'VAT Report'
#                     }
            
    
class AccountTaxReport(models.TransientModel):
    _inherit = 'account.tax.report'
    _description = 'Tax Report'

    def _print_report(self, data):
        return self.env.ref('sipa_tax_report.report_account_tax').report_action(self, data=data)

#     def export_detail_pdf(self):
#         data = {}
#         data['form'] = self.read()[0]
#         return self.env.ref('sipa_tax_report.report_account_tax').report_action(self, data=data)
    
    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
                return self.env.ref('sipa_tax_report.report_tax_xlsx').report_action(self, data=datas)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
