# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    @api.multi
    def button_confirm(self):        
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.user.company_id.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today())):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
                
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
    
#         template = self.env.ref('purchase_approval.purchase_order_confirm_email_template', False)
#         template_id = self.env['mail.template'].browse(template.id)
#         template_id.with_context(url=base_url).send_mail(self.id)
        
#         mail_send_bool = self.company_id.purchase_approve_active
#         purchase_order_bool = self.company_id.po_double_validation
        
#         print("333333333333333333333333333",mail_send_bool,purchase_order_bool)
#         print("333333333333333333333333333",mail_send_bool2)
        
        mail_send = self.env['ir.config_parameter'].sudo().get_param('purchase_approval.mail_send_to')
        if mail_send !='[]':
            line = mail_send.strip('][').split(', ')
            
            email_list = []
            for vals in line:
                mail_users = self.env['res.users'].browse(int(vals))
                    
                email_to = mail_users.partner_id.email if mail_users.partner_id else ''
                if email_to:
                    email_list.append(email_to)
            if email_list:
                email_list_new = ','.join( c for c in email_list if  c not in "[]''")
                template = self.env.ref('purchase_approval.purchase_order_confirm_email_template', False)
                template_id = self.env['mail.template'].browse(template.id)
                template_id.with_context(url=base_url,mail=email_list_new).send_mail(self.id, force_send=True)
        
        return True
    
    @api.multi
    def button_approve(self):
        
        res = super(PurchaseOrder, self).button_approve()
        if self.company_id.purchase_approve_active:
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)
            
            approved_mail_send = self.env['ir.config_parameter'].sudo().get_param('purchase_approval.approved_mail_send_to')
            approved_line = approved_mail_send.strip('][').split(', ') 
            
            if approved_mail_send !='[]':
                email_list = []
                for vals in approved_line:
                    mail_users = self.env['res.users'].browse(int(vals))
                        
                    email_to = mail_users.partner_id.email if mail_users.partner_id else ''
                    if email_to:
                        email_list.append(email_to)
                
                if email_list:
                    email_list_new = ','.join( c for c in email_list if c not in "[]''")
                    template = self.env.ref('purchase_approval.purchase_order_approve_email_template', False)
                    template_id = self.env['mail.template'].browse(template.id)
                    template_id.with_context(url=base_url,mail=email_list_new).send_mail(self.id, force_send=True)
        
        return res
        
        
        
        