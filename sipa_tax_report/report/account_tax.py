# -*- coding: utf-8 -*-

# from io import BytesIO

from odoo import api, models, _
from odoo.exceptions import UserError


# class ReportTax(models.AbstractModel):
#     _inherit = 'report.accounting_pdf_reports.report_tax'
# 
# 
#     @api.model
#     def get_lines(self, options):
#         taxes = {}
#         for tax in self.env['account.tax'].search([('type_tax_use', '!=', 'none')]):
#             if tax.children_tax_ids:
#                 for child in tax.children_tax_ids:
#                     if child.type_tax_use != 'none':
#                         continue
#                     taxes[child.id] = {'tax': 0, 'net': 0, 'name': child.name, 'type': tax.type_tax_use}
#             else:
#                 taxes[tax.id] = {'tax': 0, 'net': 0, 'name': tax.name, 'type': tax.type_tax_use}
#         self.with_context(date_from=options['date_from'], date_to=options['date_to'], company_id=options['company_id'][0], strict_range=True)._compute_from_amls(options, taxes)
#         groups = dict((tp, []) for tp in ['sale', 'purchase'])
#         for tax in taxes.values():
#             if tax['tax']:
#                 groups[tax['type']].append(tax)
#         return groups
    

class ReportTax(models.AbstractModel):
    _name = 'report.sipa_tax_report.report_tax'


    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
#         print ("\n Form ; ", data.get('form'))
        date_from = data['form'].get('date_from')
        date_to = data['form'].get('date_to')
        company_id = data['form'].get('company_id')[0]
#         print ("\ndata ; ", data)
        return {
            'data': data['form'],
            'lines': self.get_lines(date_from, date_to, company_id),
        }


        
    @api.multi
    def get_lines(self, date_from, date_to, company_id):
        query = """
            SELECT a.name AS name, a.ref AS ref, m.date AS date, t.amount AS amount, 
                CASE WHEN COALESCE(SUM(m.debit-m.credit), 0) > 0.0 AND t.type_tax_use = 'sale' THEN -1 *  m.tax_base_amount
                WHEN COALESCE(SUM(m.debit-m.credit), 0) <  0.0 AND t.type_tax_use = 'purchase' THEN -1 * m.tax_base_amount 
                ELSE m.tax_base_amount END AS base_amount, 
                CASE WHEN t.type_tax_use = 'sale' THEN -1 * COALESCE(SUM(m.debit-m.credit), 0) ELSE COALESCE(SUM(m.debit-m.credit), 0) END AS Tax,              
                CASE WHEN COALESCE(SUM(m.debit-m.credit), 0) > 0.0 AND t.type_tax_use = 'sale' THEN -1 * a.amount
                WHEN COALESCE(SUM(m.debit-m.credit), 0) <  0.0 AND t.type_tax_use = 'purchase'  THEN -1 * a.amount ELSE a.amount END AS Total, 
                t.name AS tax, t.id AS tax_id, t.type_tax_use as tax_type, m.partner_id AS partner_id
                     
                FROM account_move_line AS m
                INNER JOIN account_tax t ON (m.tax_line_id = t.id)           
                INNER JOIN account_move a ON (m.move_id = a.id)
                INNER JOIN res_company c ON (m.company_id = c.id)
                WHERE (a.date >= %s) AND (a.date <= %s) AND m.tax_exigible AND c.id = %s
                GROUP BY m.id, a.id, t.id
                ORDER BY m.date;
        """
                     
        self.env.cr.execute(query, (date_from, date_to, company_id))
        results = self.env.cr.fetchall()
        
#         print ("Res ; ", results)
        
        groups = dict((tp, {}) for tp in ['sale', 'purchase', 'all'])
        sale_groups = dict((tp[8], []) for tp in results if tp[9] == 'sale')
        pur_groups = dict((tp[8], []) for tp in results if tp[9] == 'purchase')
        groups['sale'] = sale_groups
        groups['purchase'] = pur_groups
          
        taxes = dict((t[3], {'sale': [0.0, 0.0, 0.0], 'purchase': [0.0, 0.0, 0.0]}) for t in results)
  
        partner_obj = self.env['res.partner']
        for line in results:
            line_vals = list(line)
            if line[10]:
                partner_id = partner_obj.browse(line[10]).sudo()
                line_vals.insert(3, partner_id.name)
                line_vals.insert(4, partner_id.vat)
            else:
                line_vals.insert(3, '')
                line_vals.insert(4, '')
            groups[line[9]][line[8]].append(line_vals)
            
            taxes[line[3]][line[9]][0] += line[4]
            taxes[line[3]][line[9]][1] += line[5]
            taxes[line[3]][line[9]][2] += line[6]

        for tax in taxes:
            taxes[tax]['sale'][2] = taxes[tax]['sale'][0] + taxes[tax]['sale'][1]
            taxes[tax]['purchase'][2] = taxes[tax]['purchase'][0] + taxes[tax]['purchase'][1]

        groups['all'] = taxes
             
#         print ("Grps ; ", groups)
#         print (Errrrrrrr)
        return groups
