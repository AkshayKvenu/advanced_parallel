
from odoo import api, fields, models, _
from datetime import date
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class JournalItemsAmortization(models.Model):
    _name = 'journal.items.amortization'
    
    @api.depends('debit', 'credit')
    def _store_balance(self):
        for line in self:
            line.balance = line.debit - line.credit
            
    account_id = fields.Many2one('account.account', string="Account")
    partner_id = fields.Many2one('res.partner', string="Partner")
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tag')
    debit = fields.Float("Debit")
    credit = fields.Float("Credit")
    label = fields.Char("Label")
    balance = fields.Float(compute='_store_balance')
    asset_id_amortization = fields.Many2one('account.asset.asset.amortization', string='Asset', required=True, ondelete='cascade')
    
            
    @api.constrains('debit','credit')
    def debit_credit_validation(self):
        if self.credit > 0.0 and self.debit > 0.0:
                raise UserError(_('Wrong credit or debit value in entry lines! Credit or debit should be zero. '))
        if self.credit == 0.0 and self.debit == 0.0:
                raise UserError(_('Wrong credit or debit value in entry lines! Both Credit and debit should not be zero. '))
    
    
    @api.model
    def create(self, vals):
        result = super(JournalItemsAmortization, self).create(vals)
        if 'balance' in vals:
            if vals['balance'] != 0.0:
                raise UserError(_('Cannot create unbalanced journal entry'))
        return result
    
    @api.model
    def write(self, vals):
        result = super(JournalItemsAmortization, self).write(vals)
        if 'balance' in vals:
            if vals['balance'] != 0.0:
                raise UserError(_('Cannot create unbalanced journal entry'))
        return result
                    
    
class AmortizationLineItems(models.Model):
    _name = 'amortization.line.items'
    
    date = fields.Date("Date")
    move_id = fields.Many2one('account.move', string='Depreciation Entry')
    asset_id_amortization = fields.Many2one('account.asset.asset.amortization', string='Asset', required=True, ondelete='cascade')
    move_check = fields.Boolean(compute='_get_move_check', string='Linked', track_visibility='always', store=True)
    sequence = fields.Integer(required=True)
    move_posted_check = fields.Boolean(compute='_get_move_posted_check', string='Posted', track_visibility='always', store=True)
    
    parent_state = fields.Selection(related='asset_id_amortization.state', string='State of Asset', readonly=False)
    
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

    @api.multi
    def _cron_entry_list(self, post_move=True):
        created_moves = self.env['account.move']
        amortization_line_obj = self.search([('move_id','=', False),('parent_state','=','open')])
        for line in amortization_line_obj:
            if line.date <= date.today():
                move_vals = self._prepare_move(line)
                move = self.env['account.move'].create(move_vals)
                if line.asset_id_amortization.auto_post_entry:
                    move.action_post()
                line.write({'move_id': move.id, 'move_check': True})
                created_moves |= move

    def _prepare_move(self, line):
        move_lines = []
        for lines in line.asset_id_amortization.journal_items_ids:
#             asset_name = line.asset_id_amortization.name + ' (%s/%s)' % (line.sequence, len(line.asset_id_amortization.entry_line_ids))
            move_line = {
                'name': lines.label,
                'account_id': lines.account_id.id,
                'debit': lines.debit,
                'credit': lines.credit,
                'partner_id': lines.partner_id.id,
                'analytic_account_id': lines.account_analytic_id.id,
                # 'analytic_tag_ids': [(6, 0, analytic_tag_ids.ids)] if category_id.type == 'sale' else False,
#                 'currency_id': company_currency != current_currency and current_currency.id or False,
#                 'amount_currency': company_currency != current_currency and - 1.0 * lines.amount or 0.0,
            }
            move_lines.append((0, 0, move_line))
#             }
        asset_name = line.asset_id_amortization.name + ' (%s/%s)' % (line.sequence, len(line.asset_id_amortization.entry_line_ids))
        move_vals = {
            'ref': asset_name,
            'date': line.date or False,
            'journal_id': line.asset_id_amortization.journal_id.id or 3,
            'line_ids': move_lines,
        }
        return move_vals