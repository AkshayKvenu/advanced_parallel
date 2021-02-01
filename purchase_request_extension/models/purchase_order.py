# Copyright 2018-2019 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError
from num2words import num2words
import math


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    @api.constrains('order_line')
    def compute_product_qty(self):
        if self.state == 'purchase':
            pr_lines = self.env['purchase.request.line'].search([])
            pr_obj = self.env['purchase.request']
            print("1111111111112222222222222333333333")
            order_line_ids = []
            for lines in pr_lines:
                for po_lines in lines.purchase_lines:
                    order_id = po_lines.order_id
                    if self.id == order_id.id:
                        pr_obj = lines.request_id
            flag = 0
            print("qqqqqqqqqqqqqqqqqqqqqqqqqqq",pr_obj)
            if pr_obj:
                for pr_line in pr_obj.line_ids:
                    for po_line in pr_line.purchase_lines:
                        if po_line.order_id.id != self.id and po_line.order_id.state == 'purchase':
                            order_line_ids.append(po_line.id)
                
                print("rrrrrrrrrrrrrrrrrrrrrrr",order_line_ids)
                for rec in self.order_line:
                    request_lines = self.env['purchase.order.line'].search([('id','in',order_line_ids),('product_id','=',rec.product_id.id)])
                    total_qty_po = 0
                    total_done_qty = 0
                    print("ttttttttttttttttttt",request_lines)
                    for req_obj in request_lines:
                        total_qty_po += req_obj.product_qty
    #                     for purchase_lines in req_obj.purchase_lines:
                        for move in req_obj.move_ids:
                            if move.state != 'cancel':
                                total_done_qty += move.product_uom_qty
                                    
    
                    total_qty_pr = 0
                    
                    for pr_line in pr_obj.line_ids:
                        if pr_line.product_id == rec.product_id:
                            total_qty_pr += pr_line.product_qty
#                     print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwww",total_done_qty,rec.product_qty, total_qty_pr)
                    print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwww",total_qty_po+rec.product_qty, total_qty_pr)
                    print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwww",rec.purchase_request_lines.id)
                    if total_qty_po+rec.product_qty > total_qty_pr:
                        raise UserError(
                            _('%s product Quantity exceeds by %s.')% (rec.product_id.name,(total_qty_po+rec.product_qty)-total_qty_pr))
                    if total_qty_po+rec.product_qty < total_qty_pr:
                        if rec.purchase_request_lines.id != False:
                            flag = 1
                            print("ooooooooooooooo")
                            if pr_obj.state == 'done':
                                print("pppppppppppppppppppp")
                                pr_obj.button_reset_to_approve()
#                     if total_qty_po+rec.product_qty == total_qty_pr:
#                         if pr_obj.state == 'approved':
#                             pr_obj.button_done()
                
                for pr in pr_obj.line_ids:
                    if pr.purchase_state != 'purchase':
                        flag = 1
                        break
                print("hhhhhhhhhhhhhhhhhhhhhhhhhhh",flag)
                if flag == 0:
                    pr_obj.write({'state': 'done'})
                                            

    @api.multi
    def button_approve(self):
        res = super(PurchaseOrder, self).button_approve()
        if 'purchase_approve_active' in self.env['res.company']._fields and self.company_id.purchase_approve_active:
            print("Aaaaaaaaaaaaaaaaaa",self.state)
            if self.state == 'approved':
                print("    Aaaaaaaaaaaaaaaaaa1111111")
                return res
        self.confirm_pr_()
        return res
    
    @api.multi
    def button_release(self):
        res = super(PurchaseOrder, self).button_release()
        self.confirm_pr_()
        return res
    
    def confirm_pr_(self):
        pr_lines = self.env['purchase.request.line'].search([])
        pr_obj = self.env['purchase.request']
        print("1111111111112222222222222333333333")
        order_line_ids = []
        for lines in pr_lines:
            for po_lines in lines.purchase_lines:
                order_id = po_lines.order_id
                if self.id == order_id.id:
                    pr_obj = lines.request_id
        flag = 0
        print("qqqqqqqqqqqqqqqqqqqqqqqqqqq",pr_obj)
        if pr_obj:
            for pr_line in pr_obj.line_ids:
                for po_line in pr_line.purchase_lines:
                    if po_line.order_id.id != self.id and po_line.order_id.state == 'purchase':
                        order_line_ids.append(po_line.id)
            
            print("rrrrrrrrrrrrrrrrrrrrrrr",order_line_ids)
            for rec in self.order_line:
                request_lines = self.env['purchase.order.line'].search([('id','in',order_line_ids),('product_id','=',rec.product_id.id)])
                total_qty_po = 0
                total_done_qty = 0
                print("ttttttttttttttttttt",request_lines)
                for req_obj in request_lines:
                    total_qty_po += req_obj.product_qty
#                     for purchase_lines in req_obj.purchase_lines:
                    for move in req_obj.move_ids:
                        if move.state != 'cancel':
                            total_done_qty += move.product_uom_qty
                                

                total_qty_pr = 0
                
                for pr_line in pr_obj.line_ids:
                    if pr_line.product_id == rec.product_id:
                        total_qty_pr += pr_line.product_qty
                print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwww",total_done_qty,rec.product_qty, total_qty_pr)
#                 print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwww",total_done_qty,rec,rec.product_qty, total_qty_pr1)
                if total_qty_po+rec.product_qty > total_qty_pr:
                    raise UserError(
                        _('%s product Quantity exceeds by %s.')% (rec.product_id.name,(total_qty_po+rec.product_qty)-total_qty_pr))
                    
                    
#             for rec in self.order_line:
#                 request_lines = self.env['purchase.order.line'].search([('id','in',order_line_ids),('product_id','=',rec.product_id.id)])
                
                
                
            for pr in pr_obj.line_ids:
                if pr.purchase_state != 'purchase':
                    print("lllllllllllllllllllllllllll",pr.purchase_state)
                    flag = 1
                    break
            if flag == 0:
                pr_obj.write({'state': 'done'})
        
        

class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request"


    def button_reset_to_approve(self):
        if self.state == 'done':
            self.write({'state':'approved'})

class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    item_code = fields.Char('Code', track_visibility='onchange')
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            name = self.product_id.name
            if self.product_id.code:
                self.item_code = self.product_id.code
            if self.product_id.description_purchase:
                name = '[%s] %s' % (name, self.product_id.description_purchase)
#                 name += '\n' + self.product_id.description_purchase
            self.product_uom_id = self.product_id.uom_id.id
            self.product_qty = 1
            self.name = name
#     
#     @api.one
#     @api.depends('amount_total')
#     def _compute_amount_words(self):
#         lang = self.env.user.lang
# #         number_dec = 0
#         number_dec = str(self.amount_total).split('.')[1]
#         print('nnnmmm',self.amount_total)
#         numb = int(number_dec[0])
#         numb1 = int(number_dec[1]) if len(number_dec) > 1 else 0
#         number_dec = int(number_dec)
#         self.amount_words = (num2words(math.floor(self.amount_total), lang=lang) +"  "+ self.currency_id.currency_unit_label).title()
#         
#         if number_dec > 0:
#             if numb!=0 and numb1 == 0:
#                 number_dec *= 10
#             self.amount_words += "  and  " + (num2words(math.floor(number_dec), lang=lang) +"  "+ self.currency_id.currency_subunit_label).title()
#     amount_words=fields.Char(string='Total in words:',compute='_compute_amount_words')

