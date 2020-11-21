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
from odoo.exceptions import ValidationError, UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_is_zero, float_compare
from datetime import datetime
import calendar

        
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    sale_type = fields.Selection([('trade', 'Trading'), ('rent', 'Rental')], 'Sale Type', default = 'trade')
    collective_number = fields.Char(string = "Collective Number")
    
    
    @api.multi
    def _action_confirm(self):
        """ On SO confirmation, some lines should generate a task or a project. """
        result = super(SaleOrder, self)._action_confirm()
        self.mapped('order_line').sudo().with_context(
            default_company_id = self.company_id.id,
            force_company = self.company_id.id,
        )._rental_project_generation()
        if self.sale_type == 'rent' and self.analytic_account_id:
            parent_account = self.env['account.analytic.account'].search([('is_rental_account', '=', True)], limit = 1)
            self.analytic_account_id.parent_id = parent_account.id
#             self.analytic_account_id.update({'active': False})
        return result
        
    @api.onchange('sale_type')
    def _change_type_clear_lines(self):
        self.order_line = False
        
    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        references = {}
        invoices_origin = {}
        invoices_name = {}

        # Keep track of the sequences of the lines
        # To keep lines under their section
        inv_line_sequence = 0
        for order in self:
            group_key = order.id if grouped else (order.partner_invoice_id.id, order.currency_id.id)

            # We only want to create sections that have at least one invoiceable line
            pending_section = None

            # Create lines in batch to avoid performance problems
            line_vals_list = []
            timesheet_list = []
            # sequence is the natural order of order_lines
            for line in order.order_line:
                invoice = False
                qty_to_invoice = 0.0
                tasks = False
                if line.sale_type == 'rent' and line.project_id:
                    tasks = self.env['project.task'].search([('sale_line_id', '=', line.id), ('project_id', '=', line.project_id.id)])
                    qty_to_invoice = len(tasks.ids)
                else:
                    qty_to_invoice = line.qty_to_invoice
                if line.display_type == 'line_section':
                    pending_section = line
                    continue
                if float_is_zero(qty_to_invoice, precision_digits=precision):
                    continue
                if group_key not in invoices:
                    inv_data = order._prepare_invoice()
                    invoice = inv_obj.create(inv_data)
                    references[invoice] = order
                    invoices[group_key] = invoice
                    invoices_origin[group_key] = [invoice.origin]
                    invoices_name[group_key] = [invoice.name]
                elif group_key in invoices:
                    if order.name not in invoices_origin[group_key]:
                        invoices_origin[group_key].append(order.name)
                    if order.client_order_ref and order.client_order_ref not in invoices_name[group_key]:
                        invoices_name[group_key].append(order.client_order_ref)

                if line.sale_type == 'rent':
                    for tk in tasks:
                        rent_line = line._rent_invoice_line_vals(tk, invoices[group_key].id)
                        for rline in rent_line['line']:
                            inv_line_sequence += 1
                            rline['sequence'] = inv_line_sequence
#                         )
                        line_vals_list.extend(rent_line['line'])
                        timesheet_list.extend(rent_line['timesheets'])        
                        for sheet in rent_line['timesheets']:  
                            sheet.write({'timesheet_invoice_id': invoices[group_key].id, })                  
                        
                else:
                    if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final):
                        if pending_section:
                            section_invoice = pending_section.invoice_line_create_vals(
                                invoices[group_key].id,
                                pending_section.qty_to_invoice
                            )
                            inv_line_sequence += 1
                            section_invoice[0]['sequence'] = inv_line_sequence
                            line_vals_list.extend(section_invoice)
                            pending_section = None
    
                        inv_line_sequence += 1
                        inv_line = line.invoice_line_create_vals(
                            invoices[group_key].id, line.qty_to_invoice
                        )
                        inv_line[0]['sequence'] = inv_line_sequence
                        line_vals_list.extend(inv_line)

            if references.get(invoices.get(group_key)):
                if order not in references[invoices[group_key]]:
                    references[invoices[group_key]] |= order

            self.env['account.invoice.line'].create(line_vals_list)

        for group_key in invoices:
            invoices[group_key].write({'name': ', '.join(invoices_name[group_key]),
                                       'origin': ', '.join(invoices_origin[group_key])})
            sale_orders = references[invoices[group_key]]
            if len(sale_orders) == 1:
                invoices[group_key].reference = sale_orders.reference

        if not invoices:
            raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

        self._finalize_invoices(invoices, references)
        return [inv.id for inv in invoices.values()]
     
     
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    rental_qty = fields.Integer('Period', default=1)  
    sale_type = fields.Selection([('trade', 'Trading'), ('rent', 'Rental')], 'Sale Type', default='trade')
    rental_uom_id = fields.Many2one('uom.uom', 'Rental Unit of Measure', help="Default unit of measure used for rental operations.")
    part_number = fields.Char(string="Part Number")
    
    @api.multi
    @api.onchange('product_id')
    def product_part_number(self):
        if self.product_id:
            self.part_number = self.product_id.default_code
            name = self.product_id.name
            if self.product_id.description_sale:
                name+= '\n' + self.product_id.description_sale
            self.name = name

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(SaleOrderLine, self).create(vals_list)
        # Do not generate task/project when expense SO line, but allow
        # generate task with hours=0.
        for line in lines:
            if line.state == 'sale' and line.product_id.is_rental:
                line.sudo()._rental_project_generation()
                # if the SO line created a task, post a message on the order
                if line.task_id:
                    msg_body = _("Task Created (%s): <a href=# data-oe-model=project.task data-oe-id=%d>%s</a>") % (line.product_id.name, line.task_id.id, line.task_id.name)
                    line.order_id.message_post(body=msg_body)
        return lines

    @api.multi
    def _rental_project_generation(self):
        order_ids = self.mapped('order_id').ids
        so_lines_with_project = self.search([('order_id', 'in', order_ids), ('project_id', '!=', False), ('product_id.is_rental', '=', True)])
        project_ids = so_lines_with_project.mapped('project_id').ids
        so_line_new_project = self.filtered(lambda sol: sol.product_id.is_rental == True)
        
        project = project_ids and project_ids[0] or False
        for so_line in so_line_new_project:
#             project = so_line.project_id
            if not project and not so_lines_with_project:
                project = so_line._timesheet_create_project()
            elif not so_line.project_id:
                so_line.project_id = project
                
    @api.onchange('product_id')
    def _get_product_domain(self):
        if self.sale_type == 'rent':
            return {'domain': {'product_id': [('is_rental', '=', True)]}}
        else:
            return {'domain': {'product_id': [('is_rental', '=', False)]}}
                
    @api.onchange('product_id')
    def _change_product_rental_uom(self):
        if self.product_id:
            self.rental_uom_id = self.product_id.rental_uom_id.id
            
    @api.depends('product_uom_qty', 'rental_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty * line.rental_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            
    def _rent_invoice_line_vals(self, task=False, invoice_id=False):
        inv_dict = {'line': [], 'timesheets': []}
        if task:
            context = self.env.context
            start_date = datetime.strptime(context.get('start_date', False), '%Y-%m-%d').date() 
            end_date = datetime.strptime(context.get('end_date', False), '%Y-%m-%d').date() 
            timesheets = task.timesheet_ids.filtered(lambda x: x.date >= start_date and x.date <= end_date and not x.timesheet_invoice_id)
            if timesheets:
                product = self.product_id.with_context(force_company=self.company_id.id)
                account = product.property_account_income_id or product.categ_id.property_account_income_categ_id
        
                if not account and self.product_id:
                    raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') % 
                        (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))
                fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
                if fpos and account:
                    account = fpos.map_account(account)
                
                month_days = calendar.monthrange(start_date.year, start_date.month)[1]
                timesheet_len = len(timesheets.ids)
                day_uom = self.env['uom.uom'].search([('period_type', '=', 'day')], limit = 1)
                month_uom = self.env['uom.uom'].search([('period_type', '=', 'month')], limit = 1)

                if timesheet_len < month_days:
                    rent_period = timesheet_len
                    rental_uom_id = day_uom
                    if self.rental_uom_id.id == day_uom.id:
                        unit_price = self.price_unit
                    else:
                        unit_price = self.price_unit / 30
                else:
                    rent_period = 1
                    rental_uom_id = month_uom
                    if self.rental_uom_id.id == month_uom.id:
                        unit_price = self.price_unit
                    else:
                        unit_price = self.price_unit * 30
                
                inv_dict['line'].append({
                        'name': self.name,
                        'sequence': self.sequence,
                        'origin': self.order_id.name,
                        'account_id': account.id,
                        'lot_id': task.lot_id.id,
                        'rent_period': rent_period,
                        'rent_uom_id': rental_uom_id.id,
                        'price_unit': unit_price,
                        'quantity': 1.0,
                        'uom_id': self.product_uom.id,
                        'product_id': self.product_id.id or False,
                        'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
                        'account_analytic_id': self.order_id.analytic_account_id.parent_id.id or False,
                        'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
                        'display_type': self.display_type,
                        'invoice_id': invoice_id,
                        'sale_line_ids': [(6, 0, [self.id])]
                    })
                inv_dict['timesheets'] = timesheets
            return inv_dict

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
