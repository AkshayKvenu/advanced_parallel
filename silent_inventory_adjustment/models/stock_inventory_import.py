import csv
from odoo import api, fields, models, _
import base64
from odoo.exceptions import ValidationError


class StockInventoryImport(models.TransientModel):
    _name = "stock.inventory.import"

    data_file = fields.Binary(string='csv File')
    file_name = fields.Char('Filename')

    def _check_csv(self, data_file):
        return data_file.strip().endswith('.csv')

    @api.multi
    def import_inventory_adjustment_csv(self):
        """
        Method to Import the Product into active Inventory
        :return:
        """
        inventory_id = self._context.get('active_id')
        stock_inventory_obj = self.env['stock.inventory']
        stock_inventory = stock_inventory_obj.search_read(domain=[('id', '=', inventory_id)])
        if stock_inventory[0].get('state') == 'confirm':
            b64 = base64.decodestring(self.data_file).decode('utf-8')
            reader = csv.DictReader(b64.split('\n'), delimiter=',')
            stock_inventory_line_obj = self.env['stock.inventory.line']
            product_obj = self.env['product.product']
            production_lot_obj = self.env['stock.production.lot']
            for row in reader:
                formatted_dict = dict(row)
                product = product_obj.search_read(domain=[('name', '=', formatted_dict.get('Product'))])
                if product:
                    line_item = {}
                    line_item['product_id'] = product[0].get('id')
                    line_item['inventory_id'] = inventory_id
                    line_item['product_qty'] = formatted_dict.get('Real Qty')
                    line_item['theoretical_qty'] = formatted_dict.get('Theoretical Qty')
                    if formatted_dict.get('Lot/Serial Number'):
                        production_lot_id = production_lot_obj.sudo().search(
                            [('name', '=', formatted_dict.get('Lot/Serial Number')),
                             ('product_id', '=', product[0].get('id'))])
                        if not production_lot_id:
                            production_lot_id = production_lot_obj.sudo().create(
                                {'name': formatted_dict.get('Lot/Serial Number'), 'product_id': product[0].get('id')})
                        line_item['prod_lot_id'] = production_lot_id.id
                    else:
                        line_item['prod_lot_id'] = None
                    line_obj = stock_inventory_line_obj.search(
                        [('inventory_id', '=', inventory_id), ('product_id', '=', product[0].get('id'))])
                    if line_obj:
                        line_obj[0].write(line_item)
                    else:
                        line_item['location_id'] = stock_inventory[0].get('location_id')[0]
                        stock_inventory_line_obj.create(line_item)
            return True
        else:
            raise ValidationError(_('Inventory needs to be in progress State.'))

    @api.multi
    def import_file(self):
        if self.file_name:
            if not self._check_csv(self.file_name):
                raise ValidationError(_('Unsupported file format, Import only supports CSV'))
            return self.import_inventory_adjustment_csv()
        else:
            raise ValidationError(_('Please Select the CSV file'))