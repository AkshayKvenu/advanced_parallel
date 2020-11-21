
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ReportAction(models.Model):
    _inherit = 'ir.actions.report'
    

    @api.model
    def run_html_scheduler(self):
        for rec in self.search([]):
            if rec.report_type == 'qweb-pdf':
                rec.report_type = 'qweb-html'