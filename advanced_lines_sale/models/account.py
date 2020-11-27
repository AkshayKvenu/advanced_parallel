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
from odoo.exceptions import UserError


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    
    lot_id = fields.Many2one('stock.production.lot', 'Serial #')
    rent_period = fields.Integer('Period', default=1.0)
    rent_uom_id = fields.Many2one('uom.uom', 'Rental Unit of Measure', help="Default unit of measure used for rental operations.")
    part_number = fields.Char(string="Part Number")
    
    
    @api.multi
    @api.onchange('product_id')
    def product_part_number(self):
        if self.product_id:
            self.part_number=self.product_id.default_code
            name = self.product_id.name
            if self.product_id.description_sale:
                name+= '\n' + self.product_id.description_sale
            self.name = name
    
    
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity * (self.rent_period or 1.0), product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price * (self.rent_period or 1.0)
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(price_subtotal_signed, self.invoice_id.company_id.currency_id, self.company_id or self.env.user.company_id, date or fields.Date.today())
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    
    @api.multi
    def unlink(self):
        if any(line.timesheet_invoice_id for line in self):
            raise UserError(_("You cannot delete a timesheet which is invoiced."))
        res = super(AnalyticLine, self).unlink()
        return res

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    is_unique = fields.Boolean('Is Unique',default=False)
    payment_voucher_id = fields.Many2one('payment.voucher','Payment Voucher', copy=False)
    amount_to_pay = fields.Float('Amount to Pay', store=True)
    
#     @api.one
#     @api.depends('residual')
#     def _compute_amount_pay(self):
#         self.amount_to_pay = self.residual
    
    @api.multi
    def write(self, vals):
        if 'amount_to_pay' in vals:
            if vals['amount_to_pay'] > self.residual:
                raise UserError(_("Amount to pay should not be greater than Amount due."))
                
        return super(AccountInvoice, self).write(vals)

    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        round_curr = self.currency_id.round
        for line in self.invoice_line_ids:
            if not line.account_id:
                continue
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity * (line.rent_period or 1.0), line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                    tax_grouped[key]['base'] = round_curr(val['base'])
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += round_curr(val['base'])
        return tax_grouped


class PaymentVoucher(models.Model):
    _name = 'payment.voucher'
    
    name = fields.Char(string='Payment Voucher Reference',copy=False, readonly=True)
    vendor_id = fields.Many2one('res.partner','Vendor')
    voucher_date = fields.Date('Voucher Date')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Awaiting Payment'), ('paid', 'Paid')], default='draft', string='Status')
    invoices_ids = fields.Many2many('account.invoice')
    company_id = fields.Many2one('res.company','Company',default = lambda self: self.env.user.company_id)
        
        
    total_amount_due = fields.Float('Amount Due', compute='_compute_total_amount_due',readonly=True)
    total_amount_to_pay = fields.Float('Amount To Pay', compute='_compute_total_amount_pay',readonly=True)
#     amount_to_pay = fields.Float('Amount To Pay')
    total_invoice_amount = fields.Float('Invoice Amount',readonly=True)
    
    payment_voucher_line_ids = fields.One2many('payment.voucher.lines', 'payment_voucher_id', string="Payment Voucher Lines")
        
    @api.depends('invoices_ids')
    def _compute_total_amount_pay(self):
        for rec in self:
            for line in rec.payment_voucher_line_ids:
                rec.total_amount_to_pay += line.amount_to_pay
        
    @api.depends('invoices_ids')
    def _compute_total_amount_due(self):
        for rec in self:
            for line in rec.payment_voucher_line_ids:
                rec.total_amount_due += line.amount_due
        
        
                
    @api.onchange('vendor_id')
    def invoiceids_clear(self):
        self.invoices_ids=False
        self.payment_voucher_line_ids=False
        
        
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('payment.voucher') or _('New')
        result = super(PaymentVoucher, self).create(vals)
        result.total_amount_due=0
        result.total_invoice_amount=0
        result.total_amount_to_pay=0
        for line in result.payment_voucher_line_ids:
#             line.payment_voucher_id=result.id
            result.total_amount_due=result.total_amount_due+line.amount_due
            result.total_invoice_amount=result.total_invoice_amount+line.invoice_amount
            result.total_amount_to_pay=result.total_amount_to_pay+line.amount_to_pay
        vals['company_id'] = self.env.user.company_id
            
        return result
    
    @api.multi
    def write(self, vals):
#         for line in self.invoices_ids:
#             line.payment_voucher_id=False
        
        result = super(PaymentVoucher, self).write(vals)
        total_amount=0
        total_invoice=0
        total_amount_to_pay=0
        for line in self.payment_voucher_line_ids:
#             line.payment_voucher_id=self.id
            total_amount=total_amount+line.amount_due
            total_invoice=total_invoice+line.invoice_amount
            total_amount_to_pay=total_amount_to_pay+line.amount_to_pay
        vals['total_amount_due'] = total_amount
        vals['total_invoice_amount'] = total_invoice
        vals['total_amount_to_pay'] = total_amount_to_pay
        
#         result = super(PaymentVoucher, self).write(vals)
        return result

    
    def action_confirm_payment_voucher(self):
        for line in self.payment_voucher_line_ids:
            if line.invoice_id.amount_to_pay+line.amount_to_pay > line.invoice_id.residual_signed:
                raise UserError(_("Amount to pay exceeds Amount due."))
#         self.state = 'open'
        for line in self.invoices_ids:
            if line.payment_voucher_id.id != False:
                raise UserError(_("%s is already selected in another voucher.") % (line.number,))
            else:
                line.payment_voucher_id = self
#                 self.env['account.invoice'].browse(line.id).payment_voucher_id=self.id
        self.state = 'open'
                
        
     
    def action_paid_payment_voucher(self):
        for line in self.payment_voucher_line_ids:
#             if line.payment_voucher_id and line.payment_voucher_id!=self:
#                 raise UserError(_("%s is already selected in another voucher.") % (line.number,))
#             else:
# #                 self.env['account.invoice']
#                 line.payment_voucher_id = self
            if line.invoice_id.amount_to_pay+line.amount_to_pay > line.invoice_id.residual_signed:
                raise UserError(_("Amount to pay exceeds."))
                
            line.invoice_id.amount_to_pay += line.amount_to_pay
        self.state = 'paid'
     
    @api.onchange('invoices_ids') 
    def setamount(self):
        self.total_amount_due=0
        self.total_invoice_amount=0
        for amount in self.invoices_ids:
            self.total_amount_due=self.total_amount_due+amount.residual_signed
            self.total_invoice_amount=self.total_invoice_amount+amount.amount_total_signed
        
     
    @api.constrains('payment_voucher_line_ids') 
    def line_invoice_validation(self):
        invoices = []
        for voucher_line in self.payment_voucher_line_ids:
            invoices.append(voucher_line.invoice_id.id)
        print(invoices)
        if any(invoices.count(x) > 1 for x in invoices):
            raise UserError(_("Invoice is alreday used"))
            
            
            

class PaymentVoucherLines(models.Model):
    _name = 'payment.voucher.lines'
    
    vendor_id = fields.Many2one('res.partner','Vendor')
#                                 , related='payment_voucher_id.vendor_id')
    
    invoice_id = fields.Many2one('account.invoice', string='Inovice')
#     , domain=_get_domain_inovice)
    date_invoice = fields.Date('Inovice Date', related='invoice_id.date_invoice')
    date_due = fields.Date('Due Date', related='invoice_id.date_due')
    invoice_amount = fields.Monetary('Inovice Amount', related='invoice_id.amount_total_signed')
    amount_due = fields.Monetary('Amount Due', related='invoice_id.residual_signed')
    currency_id = fields.Many2one('res.currency', string='Currency', related='invoice_id.currency_id')
    amount_to_pay = fields.Monetary('Amount to pay')
    invoice_amount_to_pay = fields.Float('Amount to pay in invoice', related='invoice_id.amount_to_pay')
    
    payment_voucher_id = fields.Many2one('payment.voucher','Payment Voucher', copy=False)

    @api.onchange('invoice_id') 
    def amount_to_pay_onchange(self):
        if self.invoice_id:
            if self.invoice_id.amount_to_pay == self.invoice_id.residual_signed:
                    raise UserError(_("Invoice no amount to pay ."))
                
            line_obj = self.search([('invoice_id','=',self.invoice_id.id)])
            for line in line_obj:
                if line.payment_voucher_id and line.payment_voucher_id.state != 'paid':
                    raise UserError(_("Invoice is alreday used."))
                
                    
                    
            self.amount_to_pay = self.invoice_id.residual_signed - self.invoice_id.amount_to_pay
        
     
    @api.constrains('amount_to_pay') 
    def amount_to_pay_validation(self):
        for rec in self:
            if rec.amount_to_pay > rec.amount_due:
                raise UserError(_("Amount to pay should not be greater than Amount due."))
            
    @api.model
    def write(self, vals):
        if 'amount_to_pay' in vals:
            if vals['amount_to_pay'] > self.amount_due:
                raise UserError(_("Amount to pay should not be greater than Amount due."))
        
        return super(PaymentVoucherLines, self).write(vals)
        
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: