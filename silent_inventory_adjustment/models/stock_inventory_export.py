from odoo import api, fields, models


class StockInventoryExport(models.Model):
    _name = "stock.inventory.export"

    @api.multi
    def export_inventory_adjustment_csv(self):
        """
        Method to IDS and Redirect to the URL
        :return:
        """
        return {
            'context': self._context,
            'data': {'ids': self._context.get('active_ids')},
            'type': 'ir.actions.report',
            'report_type': 'qweb-csv',
        }
