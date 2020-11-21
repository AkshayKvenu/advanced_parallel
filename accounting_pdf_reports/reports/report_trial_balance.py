# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportTrialBalance(models.AbstractModel):
    _name = 'report.accounting_pdf_reports.report_trialbalance'

    def _get_accounts(self, accounts, display_account, target_move):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """
        
        context = dict(self.env.context)
        account_result = {}
        
        company_id = context.get('company_id', False)[0]
        date_from = context.get('date_from', False)
        date_to = context.get('date_to', False)
        analytic_accounts = context.get('account_analytic_ids', False)
        
        if analytic_accounts:
            qry_analytic = " AND ml.analytic_account_id IN %s "
        else:
            qry_analytic = " "
                
        if date_from:
            qry_init_date = "SUM(CASE WHEN ml.date < '" + date_from + "' THEN (ml.debit - ml.credit) ELSE 0.0 END)"
            date_str = " ml.date >= '" + date_from +"'"
        else:
            qry_init_date = " 0.0 "
            
        if date_from and date_to:  
            date_str += " AND "
        if date_to:
            date_str += " ml.date <= '" + date_to +"'"
            
        if date_from or date_to:
            qry_debit = "SUM(CASE WHEN " + date_str + " THEN ml.debit ELSE 0.0 END)"
            qry_credit = "SUM(CASE WHEN " + date_str + " THEN ml.credit ELSE 0.0 END)"
            qry_date = "SUM(CASE WHEN " + date_str + " THEN (ml.debit - ml.credit) ELSE 0.0 END)"
        else:
            qry_debit = "SUM(ml.debit)"
            qry_credit = "SUM(ml.credit)"
            qry_date = "SUM(ml.debit - ml.credit)"
            
        if target_move == 'posted':
            qry_target = " AND am.state = 'posted' "
        else:
            qry_target = " "

        # compute the balance, debit and credit for the provided accounts
        request = """
                SELECT ml.account_id AS id, ml.analytic_account_id, SUM(ml.debit) AS debit, SUM(ml.credit) AS credit, (SUM(ml.debit) - SUM(ml.credit)) AS balance 
                FROM account_move_line ml
                INNER JOIN account_move am ON (ml.move_id = am.id)
                LEFT OUTER JOIN account_analytic_account aa ON (ml.analytic_account_id = aa.id)
                WHERE ml.company_id = 1
                GROUP BY ml.account_id, ml.analytic_account_id
                ORDER BY ml.account_id, ml.analytic_account_id;
            """
            
        request = """SELECT a.id AS account_id, a.code AS code, a.name AS name, aa.id AS analytic_id, aa.code AS analytic_code, aa.name AS analytic_name,
            """ + qry_init_date + """ AS initial, """ + qry_debit + """ AS debit, 
            """ + qry_credit + """ AS credit, """ + qry_init_date + """ + """ + qry_date + """  AS balance
                FROM account_move_line ml
                INNER JOIN account_move am ON (ml.move_id = am.id)
                INNER JOIN account_account a ON (ml.account_id = a.id)
                LEFT OUTER JOIN account_analytic_account aa ON (ml.analytic_account_id = aa.id)
                WHERE ml.account_id IN %s AND ml.company_id = %s """
        request +=  qry_analytic + qry_target + """
                GROUP BY a.id, aa.id
                ORDER BY a.code;"""
            
#         params = (qry_init_date, qry_debit, qry_credit, qry_init_date, qry_date, tuple(accounts.ids), company_id)
        if analytic_accounts:
            params = (tuple(accounts.ids), company_id, tuple(analytic_accounts))
        else:
            params = (tuple(accounts.ids), company_id)

        self.env.cr.execute(request, params)
        results = self.env.cr.dictfetchall()
        
        account_res = {}
        for line in results:
            if display_account == 'not_zero':
                if not line['balance'] == 0.0:
                    if line['analytic_id'] in account_res:
                        account_res[line['analytic_id']].append(line)
                    else:
                        account_res[line['analytic_id']] = [line]
            else: 
                if line['analytic_id'] in account_res:
                    account_res[line['analytic_id']].append(line)
                else:
                    account_res[line['analytic_id']] = [line]
#             if display_account == 'all':
#                 if line['analytic_id'] in account_res:
#                     account_res[line['analytic_id']].append(line)
#                 else:
#                     account_res[line['analytic_id']] = [line]
#             elif display_account == 'movement' and (not line['debit'] or not line['credit']):
#                 if line['analytic_id'] in account_res:
#                     account_res[line['analytic_id']].append(line)
#                 else:
#                     account_res[line['analytic_id']] = [line]
#             elif display_account == 'not_zero' and not line['balance'] == 0.0:
#                 if line['analytic_id'] in account_res:
#                     account_res[line['analytic_id']].append(line)
#                 else:
#                     account_res[line['analytic_id']] = [line]
            
        if display_account == 'all':
            res_ids = [line['account_id'] for line in results]
            accounts_notin_res = [acc for acc in accounts if acc.id not in res_ids]
            for acc in accounts_notin_res:
                line = {'account_id': acc.id, 'code': acc.code, 'name': acc.name, 'analytic_id': None, 'analytic_code': None, 'initial': 0.0, 'debit': 0.0, 'credit': 0.0, 'balance': 0.0}
                if None in account_res:
                    account_res[None].append(line)
                else:
                    account_res[None] = [line] 
        return account_res

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        target_move = data['form'].get('target_move')
        used_context = data['form']
        accounts = docs if self.model == 'account.account' else self.sudo().env['account.account'].search([('company_id', '=', used_context['company_id'][0])])
        account_res = self.with_context(used_context)._get_accounts(accounts, display_account, target_move)
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
        }
