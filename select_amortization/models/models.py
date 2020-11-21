# -*- coding: utf-8 -*-

# from odoo import models, fields, api
# import datetime
# from dateutil.relativedelta import relativedelta

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class select_amortization_revers(models.Model):
    _inherit = 'account.move'
    select_amortization_inverse = fields.Many2one('select_amortization.select_amortization')

class account_payment(models.Model):
    _inherit = 'account.payment'
    amortization_payment = fields.Boolean(string="Amortization Payment")

# class period_rule(models.Model):
#     _name = 'period.rule'
#     name = fields.Char()
#     number_of_days = fields.Float()
#
# class select_amortization(models.Model):
#     _name = 'select_amortization.select_amortization'
#
#     name = fields.Char()
#     service_account = fields.Many2one('account.account')
#     date_from = fields.Date()
#     date_to = fields.Date()
#     period_due = fields.Float()
#     number_of_periods = fields.Float()
#     total_value = fields.Float()
#     details_entry = fields.One2many('account.move','select_amortization_inverse')
#     total_move = fields.Many2one('account.move')
#     amortization_payment = fields.Many2one('account.payment')
#     journal_id = fields.Many2one('account.journal')
#     period_rule = fields.Many2one('period.rule')
#
#
#     @api.onchange('amortization_payment')
#     def auto_fill(self):
#         if self.amortization_payment:
#             self.name = self.amortization_payment.name
#             self.total_value = self.amortization_payment.amount
#             self.journal_id = self.amortization_payment.journal_id.id
#             self.total_move = self.env['account.move'].search([('id','=',self.env['account.move.line'].search([('name','=',self.amortization_payment.name)]).move_id.id)]).id
#
#     @api.onchange('date_to')
#     def calculate_number_of_periods(self):
#         if self.date_from and self.date_to:
#             self.number_of_periods=divmod((datetime.datetime.strptime(str(self.date_to), '%Y-%m-%d')-datetime.datetime.strptime(str(self.date_from), '%Y-%m-%d')).days, self.period_rule.number_of_days)[0]
#             self.period_due = self.total_value/self.number_of_periods
#
#     # @api.model
#     # def create(self,vals):
#     #     line_ids = []
#     #     credit_line = (0,0,{
#     #     'account_id':65,
#     #     'name':vals['name']+" Service",
#     #     'debit':0.0,
#     #     'credit':vals['total_value'],
#     #     })
#     #     line_ids.append(credit_line)
#     #     debit_line = (0,0,{
#     #     'account_id':1143,
#     #     'name':vals['name']+" Service",
#     #     'debit':vals['total_value'],
#     #     'credit':0.0,
#     #     })
#     #     line_ids.append(debit_line)
#     #     total_move = self.env['account.move'].create({
#     #     'name':vals['name']+" Service",
#     #     'date':datetime.datetime.now().date(),
#     #     'ref':vals['name'],
#     #     'journal_id':3,
#     #     'company_id':1,
#     #     'line_ids':line_ids
#     #     })
#     #     vals['total_move'] = total_move.id
#     #     res = super(select_amortization,self).create(vals)
#     #     return res
#     @api.multi
#     def confirm(self):
#         counter = 1
#         while(counter<=self.number_of_periods):
#             if counter == 1:
#                 entry_month = self.date_from
#             else:
#                 entry_month = datetime.datetime.strptime(str(self.date_from), '%Y-%m-%d') + datetime.timedelta(days=(counter*self.period_rule.number_of_days+1)-self.period_rule.number_of_days+1)
#             line_ids = []
#             credit_line = (0,0,{
#             'account_id':1143,
#             'name':self.name+" Service For "+str(entry_month) ,
#             'debit':0.0,
#             'journal_id':self.journal_id.id,
#             'credit':self.total_value/self.number_of_periods,
#             })
#             line_ids.append(credit_line)
#             debit_line = (0,0,{
#             'account_id':self.service_account.id,
#             'name':self.name+" Service For "+str(entry_month) ,
#             'debit':self.total_value/self.number_of_periods,
#             'credit':0.0,
#             'journal_id':self.journal_id.id,
#             })
#             line_ids.append(debit_line)
#             total_move = self.env['account.move'].create({
#             'name':self.name+" Service For "+str(entry_month) ,
#             'date':str(entry_month),
#             'ref':self.name,
#             'journal_id':self.journal_id.id,
#             'company_id':1,
#             'select_amortization_inverse':self.id,
#             'line_ids':line_ids
#             })
#             counter+=1
#         return True
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100




class AccountAssetAsset(models.Model):
    _name = 'account.asset.asset.amortization'
    _description = 'Asset/Revenue Recognition'
    _inherit = ['mail.thread']

    debit_id = fields.Many2one('account.account')
    credit_id = fields.Many2one('account.account')
    entry_count = fields.Integer(compute='_entry_count', string='# Asset Entries')
    name = fields.Char(string='Amortization Name', required=True, readonly=True, states={'draft': [('readonly', False)]})
    code = fields.Many2one('hr.expense',string='Reference', readonly=True, states={'draft': [('readonly', False)]})
    value = fields.Float(string='Gross Value', required=True, readonly=True, digits=0, states={'draft': [('readonly', False)]}, oldname='purchase_value')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=lambda self: self.env['res.company']._company_default_get('account.asset.asset.amortization'))
    note = fields.Text()
    # category_id = fields.Many2one('account.asset.category', string='Category', required=True, change_default=True, readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date(string='Date', required=True, readonly=True, states={'draft': [('readonly', False)]}, default=fields.Date.context_today, oldname="purchase_date")
    state = fields.Selection([('draft', 'Draft'), ('open', 'Running'), ('close', 'Close')], 'Status', required=True, copy=False, default='draft',
        help="When an asset is created, the status is 'Draft'.\n"
            "If the asset is confirmed, the status goes in 'Running' and the depreciation lines can be posted in the accounting.\n"
            "You can manually close an asset when the depreciation is over. If the last line of depreciation is posted, the asset automatically goes in that status.")
    active = fields.Boolean(default=True)
    # partner_id = fields.Many2one('res.partner', string='Partner', readonly=True, states={'draft': [('readonly', False)]})
    method = fields.Selection([('linear', 'Linear'), ('degressive', 'Degressive')], string='Computation Method', required=True, readonly=True, states={'draft': [('readonly', False)]}, default='linear',
        help="Choose the method to use to compute the amount of depreciation lines.\n  * Linear: Calculated on basis of: Gross Value / Number of Depreciations\n"
            "  * Degressive: Calculated on basis of: Residual Value * Degressive Factor")
    method_number = fields.Integer(string='Number of Depreciations', readonly=True, states={'draft': [('readonly', False)]}, default=5, help="The number of depreciations needed to depreciate your asset")
    method_period = fields.Integer(string='Number of Months in a Period', required=True, readonly=True, default=12, states={'draft': [('readonly', False)]},
        help="The amount of time between two depreciations, in months")
    method_end = fields.Date(string='Ending Date', readonly=True, states={'draft': [('readonly', False)]})
    method_progress_factor = fields.Float(string='Degressive Factor', readonly=True, default=0.3, states={'draft': [('readonly', False)]})
    value_residual = fields.Float(compute='_amount_residual', method=True, digits=0, string='Residual Value')
    method_time = fields.Selection([('number', 'Number of Entries'), ('end', 'Ending Date')], string='Time Method', required=True, readonly=True, default='number', states={'draft': [('readonly', False)]},
        help="Choose the method to use to compute the dates and number of entries.\n"
             "  * Number of Entries: Fix the number of entries and the time between 2 depreciations.\n"
             "  * Ending Date: Choose the time between 2 depreciations and the date the depreciations won't go beyond.")
    prorata = fields.Boolean(string='Prorata Temporis', readonly=True, states={'draft': [('readonly', False)]},
        help='Indicates that the first depreciation entry for this asset have to be done from the asset date (purchase date) instead of the first January / Start date of fiscal year')
    depreciation_line_ids = fields.One2many('account.asset.depreciation.line.amortization', 'asset_id_amortization', string='Depreciation Lines', readonly=True, states={'draft': [('readonly', False)], 'open': [('readonly', False)]})
    salvage_value = fields.Float(string='Salvage Value', digits=0, readonly=True, states={'draft': [('readonly', False)]},
        help="It is the amount you plan to have that you cannot depreciate.")
    # invoice_id = fields.Many2one('account.invoice', string='Invoice', states={'draft': [('readonly', False)]}, copy=False)
    
    # related="category_id.type",
    @api.constrains('journal_items_ids')
    def debit_credit_validation(self):
        if self.balance != 0.0:
            raise UserError(
                _("Cannot create unbalanced journal entry.") +
                "\n\n{}{}".format(_('Difference debit - credit: '), self.balance)
            )
    
#     
    @api.depends('journal_items_ids')
    def _store_balance(self):
        debit = 0.0
        credit = 0.0
        for line in self.journal_items_ids:
            debit += line.debit
            credit += line.credit
        self.balance = debit - credit
    
    balance = fields.Float(compute='_store_balance')
    entry_type = fields.Selection([('single', 'Single Line'), ('multi', 'Multi Lines')],
                                   string='Entry Type', required=True, readonly=False, default='single')
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    
    journal_id = fields.Many2one('account.journal', string='Journal', default=3)
    # analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tag')
    date_first_depreciation = fields.Selection([
        ('last_day_period', 'Based on Last Day of Purchase Period'),
        ('manual', 'Manual')],
        string='Depreciation Dates', default='manual',
        readonly=True, states={'draft': [('readonly', False)]}, required=True,
        help='The way to compute the date of the first depreciation.\n'
             '  * Based on last day of purchase period: The depreciation dates will be based on the last day of the purchase month or the purchase year (depending on the periodicity of the depreciations).\n'
             '  * Based on purchase date: The depreciation dates will be based on the purchase date.\n')
    first_depreciation_manual_date = fields.Date(
        string='First Depreciation Date',
        readonly=True, states={'draft': [('readonly', False)]},
        help='Note that this date does not alter the computation of the first journal entry in case of prorata temporis assets. It simply changes its accounting date'
    )
    
    journal_items_ids = fields.One2many('journal.items.amortization', 'asset_id_amortization', string='Journal items amortization', readonly=True, states={'draft': [('readonly', False)], 'open': [('readonly', False)]})
    
    entry_line_ids = fields.One2many('amortization.line.items', 'asset_id_amortization', string='Amortization board', readonly=True, states={'draft': [('readonly', False)], 'open': [('readonly', False)]})
    auto_post_entry = fields.Boolean('Auto Post Entries')
    
    @api.onchange('code')
    def auto_fill(self):
        if self.code:
            if self.code.unit_amount and self.code.quantity:
                self.value = self.code.unit_amount * self.code.quantity
    @api.multi
    def open_entries(self):
        move_ids = []
        for asset in self:
            for depreciation_line in asset.depreciation_line_ids:
                if depreciation_line.move_id:
                    move_ids.append(depreciation_line.move_id.id)
        return {
        'name': _('Journal Entries'),
        'view_type': 'form',
        'view_mode': 'tree,form',
        'res_model': 'account.move',
        'view_id': False,
        'type': 'ir.actions.act_window',
        'domain': [('id', 'in', move_ids)],
        }
    def _compute_board_amount(self, sequence, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date):
        amount = 0
        if sequence == undone_dotation_number:
            amount = residual_amount
        else:
            if self.method == 'linear':
                amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                if self.prorata:
                    amount = amount_to_depr / self.method_number
                    if sequence == 1:
                        date = self.date
                        if self.method_period % 12 != 0:
                            month_days = calendar.monthrange(date.year, date.month)[1]
                            days = month_days - date.day + 1
                            amount = (amount_to_depr / self.method_number) / month_days * days
                        else:
                            days = (self.company_id.compute_fiscalyear_dates(date)['date_to'] - date).days + 1
                            amount = (amount_to_depr / self.method_number) / total_days * days
            elif self.method == 'degressive':
                amount = residual_amount * self.method_progress_factor
                if self.prorata:
                    if sequence == 1:
                        date = self.date
                        if self.method_period % 12 != 0:
                            month_days = calendar.monthrange(date.year, date.month)[1]
                            days = month_days - date.day + 1
                            amount = (residual_amount * self.method_progress_factor) / month_days * days
                        else:
                            days = (self.company_id.compute_fiscalyear_dates(date)['date_to'] - date).days + 1
                            amount = (residual_amount * self.method_progress_factor) / total_days * days
        return amount

    def _compute_board_undone_dotation_nb(self, depreciation_date, total_days):
        undone_dotation_number = self.method_number
        if self.method_time == 'end':
            end_date = self.method_end
            undone_dotation_number = 0
            while depreciation_date <= end_date:
                depreciation_date = date(depreciation_date.year, depreciation_date.month, depreciation_date.day) + relativedelta(months=+self.method_period)
                undone_dotation_number += 1
        if self.prorata:
            undone_dotation_number += 1
        return undone_dotation_number
    
    
    
    

    @api.multi
    def compute_depreciation_board(self):
        self.ensure_one()

        posted_depreciation_line_ids = self.depreciation_line_ids.filtered(lambda x: x.move_check).sorted(key=lambda l: l.depreciation_date)
        unposted_depreciation_line_ids = self.depreciation_line_ids.filtered(lambda x: not x.move_check)

        # Remove old unposted depreciation lines. We cannot use unlink() with One2many field
        commands = [(2, line_id.id, False) for line_id in unposted_depreciation_line_ids]
        commands_date = []
        if self.value_residual != 0.0 or self.entry_type == 'multi':
            amount_to_depr = residual_amount = self.value_residual

            # if we already have some previous validated entries, starting date is last entry + method period
            if posted_depreciation_line_ids and posted_depreciation_line_ids[-1].depreciation_date:
                last_depreciation_date = fields.Date.from_string(posted_depreciation_line_ids[-1].depreciation_date)
                depreciation_date = last_depreciation_date + relativedelta(months=+self.method_period)
            else:
                # depreciation_date computed from the purchase date
                depreciation_date = self.date
                if self.date_first_depreciation == 'last_day_period':
                    # depreciation_date = the last day of the month
                    depreciation_date = depreciation_date + relativedelta(day=31)
                    # ... or fiscalyear depending the number of period
                    if self.method_period == 12:
                        depreciation_date = depreciation_date + relativedelta(month=self.company_id.fiscalyear_last_month)
                        depreciation_date = depreciation_date + relativedelta(day=self.company_id.fiscalyear_last_day)
                        if depreciation_date < self.date:
                            depreciation_date = depreciation_date + relativedelta(years=1)
                elif self.first_depreciation_manual_date and self.first_depreciation_manual_date != self.date:
                    # depreciation_date set manually from the 'first_depreciation_manual_date' field
                    depreciation_date = self.first_depreciation_manual_date

            total_days = (depreciation_date.year % 4) and 365 or 366
            month_day = depreciation_date.day
            undone_dotation_number = self._compute_board_undone_dotation_nb(depreciation_date, total_days)

            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                sequence = x + 1
                amount = self._compute_board_amount(sequence, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date)
                amount = self.currency_id.round(amount)
                if float_is_zero(amount, precision_rounding=self.currency_id.rounding) and self.entry_type == "single":
                    continue
                residual_amount -= amount
                vals = {
                    'amount': amount,
                    'asset_id_amortization': self.id,
                    'sequence': sequence,
                    'name': (self.name or '') + '/' + str(sequence),
                    'remaining_value': residual_amount,
                    'depreciated_value': self.value - (self.salvage_value + residual_amount),
                    'depreciation_date': depreciation_date,
                }
                vals_date = {
                    'sequence': sequence,
                    'date':depreciation_date
                    }
                commands_date.append((0, False, vals_date))
#                 
                commands.append((0, False, vals))

                depreciation_date = depreciation_date + relativedelta(months=+self.method_period)

                if month_day > 28 and self.date_first_depreciation == 'manual':
                    max_day_in_month = calendar.monthrange(depreciation_date.year, depreciation_date.month)[1]
                    depreciation_date = depreciation_date.replace(day=min(max_day_in_month, month_day))

                # datetime doesn't take into account that the number of days is not the same for each month
                if not self.prorata and self.method_period % 12 != 0 and self.date_first_depreciation == 'last_day_period':
                    max_day_in_month = calendar.monthrange(depreciation_date.year, depreciation_date.month)[1]
                    depreciation_date = depreciation_date.replace(day=max_day_in_month)
                    
        if self.entry_type == 'single':
            self.write({'depreciation_line_ids': commands})
        elif self.entry_type == 'multi':
            self.entry_line_ids = False
            self.write({'entry_line_ids': commands_date})

        return True

    @api.multi
    def validate(self):
        if not self.journal_items_ids and self.entry_type == 'multi':
            raise UserError(_('Entry lines should not be empty'))
        self.compute_depreciation_board()
        self.write({'state': 'open'})
    @api.one
    @api.depends('value')
    def _amount_residual(self):
        total_amount = 0.0
        for line in self.depreciation_line_ids:
            if line.move_check:
                total_amount += line.amount
        self.value_residual = self.value - total_amount - self.salvage_value

    @api.multi
    @api.depends('depreciation_line_ids.move_id')
    def _entry_count(self):
        for asset in self:
            res = self.env['account.asset.depreciation.line.amortization'].search_count([('asset_id_amortization', '=', asset.id), ('move_id', '!=', False)])
            asset.entry_count = res or 0

class AccountAssetDepreciationLine(models.Model):
    _name = 'account.asset.depreciation.line.amortization'
    _description = 'Asset Depreciation Line'

    name = fields.Char(string='Depreciation Name', required=True, index=True)
    sequence = fields.Integer(required=True)
    asset_id_amortization = fields.Many2one('account.asset.asset.amortization', string='Asset', required=True, ondelete='cascade')
    parent_state = fields.Selection(related='asset_id_amortization.state', string='State of Asset', readonly=False)
    amount = fields.Float(string='Current Depreciation', digits=0, required=True)
    remaining_value = fields.Float(string='Next Period Depreciation', digits=0, required=True)
    depreciated_value = fields.Float(string='Cumulative Depreciation', required=True)
    depreciation_date = fields.Date('Depreciation Date', index=True)
    move_id = fields.Many2one('account.move', string='Depreciation Entry')
    move_check = fields.Boolean(compute='_get_move_check', string='Linked', track_visibility='always', store=True)
    move_posted_check = fields.Boolean(compute='_get_move_posted_check', string='Posted', track_visibility='always', store=True)

    @api.multi
    @api.depends('move_id')
    def _get_move_check(self):
        for line in self:
            line.move_check = bool(line.move_id)

    @api.multi
    @api.depends('move_id.state')
    def _get_move_posted_check(self):
        for line in self:
            line.move_posted_check = True if line.move_id and line.move_id.state == 'posted' else False

    @api.multi
    def _cron_generate_entries(self, post_move=True):
        created_moves = self.env['account.move']
        amortization_line_obj = self.search([('move_id','=', False),('parent_state','=','open')])
        for line in amortization_line_obj:
            if line.depreciation_date <= date.today():
                move_vals = self._prepare_move(line)
                move = self.env['account.move'].create(move_vals)
                if line.asset_id_amortization.auto_post_entry:
                    move.action_post()
                line.write({'move_id': move.id, 'move_check': True})
                created_moves |= move


    @api.multi
    def create_move(self, post_move=True):
        created_moves = self.env['account.move']
        for line in self:
            if line.move_id:
                raise UserError(_('This depreciation is already linked to a journal entry. Please post or delete it.'))
            move_vals = self._prepare_move(line)
            move = self.env['account.move'].create(move_vals)
            if line.asset_id_amortization.auto_post_entry:
                move.action_post()
            line.write({'move_id': move.id, 'move_check': True})
            created_moves |= move

        # if post_move and created_moves:
        #     created_moves.filtered(lambda m: any(m.asset_depreciation_ids.mapped('asset_id_amortization.category_id.open_asset'))).post()
        return [x.id for x in created_moves]

    def _prepare_move(self, line):
        # category_id = line.asset_id_amortization.category_id
        # account_analytic_id = line.asset_id_amortization.account_analytic_id
        # analytic_tag_ids = line.asset_id_amortization.analytic_tag_ids
        depreciation_date = self.env.context.get('depreciation_date') or line.depreciation_date or fields.Date.context_today(self)
        company_currency = line.asset_id_amortization.company_id.currency_id
        current_currency = line.asset_id_amortization.currency_id
        prec = company_currency.decimal_places
        amount = current_currency._convert(
            line.amount, company_currency, line.asset_id_amortization.company_id, depreciation_date)
        asset_name = line.asset_id_amortization.name + ' (%s/%s)' % (line.sequence, len(line.asset_id_amortization.depreciation_line_ids))
        move_line_1 = {
            'name': asset_name,
            'account_id': line.asset_id_amortization.credit_id.id,
            'debit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
            'credit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
            # 'partner_id': line.asset_id_amortization.partner_id.id,
            'analytic_account_id': line.asset_id_amortization.account_analytic_id.id,
            # 'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if category_id.type == 'sale' else False,
            'currency_id': company_currency != current_currency and current_currency.id or False,
            'amount_currency': company_currency != current_currency and - 1.0 * line.amount or 0.0,
        }
        move_line_2 = {
            'name': asset_name,
            'account_id': line.asset_id_amortization.debit_id.id,
            'credit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
            'debit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
            # 'partner_id': line.asset_id_amortization.partner_id.id,
            'analytic_account_id': line.asset_id_amortization.account_analytic_id.id,
            # 'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if category_id.type == 'purchase' else False,
            'currency_id': company_currency != current_currency and current_currency.id or False,
            'amount_currency': company_currency != current_currency and line.amount or 0.0,
        }
        move_vals = {
            'ref': line.asset_id_amortization.name,
            'date': depreciation_date or False,
            'journal_id': line.asset_id_amortization.journal_id.id or 3,
            'line_ids': [(0, 0, move_line_1), (0, 0, move_line_2)],
        }
        return move_vals
