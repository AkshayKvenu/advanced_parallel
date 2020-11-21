# -*- coding: utf-8 -*-

from ast import literal_eval
from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
       
    
    @api.multi
    def voucher_total(self):
        voucher_list=[]
        account_vouchers = self.env['account.voucher'].search([('partner_id', '=', self.partner_id.id)])
        for each in account_vouchers:
            voucher_list.append(each.partner_id.id)

        if len(voucher_list)>0:
        
            query = """
                          SELECT SUM(amount) as total, partner_id
                            FROM account_voucher
                           WHERE partner_id IN %s
                           GROUP BY partner_id
                        """ 
            params = (tuple(voucher_list),)

            self.env.cr.execute(query, params)
            price_totals = self.env.cr.dictfetchall()
            sum_total = sum(price['total'] for price in price_totals)
            self.expense_count = sum(price['total'] for price in price_totals)
        return
    
    @api.multi
    def action_view_expense(self):
        self.ensure_one()
        action = self.env.ref('account_voucher.action_purchase_receipt').read()[0]
        action['domain'] = literal_eval(action['domain'])
        action['domain'].append(('partner_id', 'child_of', self.partner_id.id))
        voucher_ids = self.env['account.voucher'].search([('partner_id', 'child_of', self.partner_id.id)])
        for object in voucher_ids:
            object.write({'account_voucher_ids': [( 4, self.id)]})
        return action
    
    expense_count = fields.Integer(string='Expense Count',compute='voucher_total', readonly=True)
    
class AccountVoucher(models.Model):
    _inherit = 'account.voucher'
    
    account_voucher_ids = fields.Many2many('account.invoice',string="Related Invoices")
    
    
#     @api.multi
#     def action_view_expense(self):
#         vouchers = self.mapped('voucher_ids')
#         action = self.env.ref('account_voucher.action_purchase_receipt').read()[0]
#         if len(vouchers) > 1:
#             action['domain'] = [('id', 'in', vouchers.ids)]
#         elif len(vouchers) == 1:
#             form_view = [(self.env.ref('account_voucher.view_purchase_receipt_form').id, 'form')]
#             if 'views' in action:
#                 action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
#             else:
#                 action['views'] = form_view
#             action['res_id'] = vouchers.ids[0]
# #         else:
# #             action = {'type': 'ir.actions.act_window_close'}
#         return action
    
#     @api.multi
#     def action_view_expense(self):
# #         list_ids = []
#         voucher_ids = self.env['account.voucher'].search([('partner_id', '=', self.partner_id.id)])
#         print("eeeeeeeeeeeeeeeeeeee",voucher_ids)
# #         for invoice in self:
# #             for depreciation_line in asset.depreciation_line_ids:
# #                 if depreciation_line.move_id:
# #                     move_ids.append(depreciation_line.move_id.id)
#         return {
#             'name': 'Expenses',
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'res_model': 'account.voucher',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'domain': [('id', '=', voucher_ids)],
#         }
    
    