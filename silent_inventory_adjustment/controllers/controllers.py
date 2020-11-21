# -*- coding: utf-8 -*-
from io import StringIO
import csv
from odoo import http
from odoo.http import Controller, route, request
import json as simplejson

class SilentErp(http.Controller):

    @route(['/report/csv'], type='http', auth="user", website=True)
    def get_csv(self, data, token):
        stock_inventory_obj = request.env['stock.inventory']
        cr = request.cr
        uid = request.uid
        data = simplejson.loads(data)
        stock_inventory = stock_inventory_obj.browse(data[0]['ids'])
        line_ids = stock_inventory.line_ids
        value_list = []
        group_production_lot_id = request.env.ref('stock.group_production_lot').id
        production_lot = request.env['ir.config_parameter'].sudo().get_param('stock.group_stock_production_lot')
        for line_item in line_ids:
            line_item_dict = {'Product': line_item.product_id.name, 'UoM': line_item.product_uom_id.name,
                              'Theoretical Qty': line_item.theoretical_qty, 'Real Qty': line_item.product_qty}

            if ((production_lot) or (group_production_lot_id in request.env.user.groups_id.ids)):
                line_item_dict['Lot/Serial Number'] = line_item.prod_lot_id.name if line_item.prod_lot_id else ' '

            value_list.append(line_item_dict)
        fp = StringIO()
        key_list = ['Product', 'UoM', 'Theoretical Qty', 'Real Qty']
        if ((production_lot) or (group_production_lot_id in request.env.user.groups_id.ids)):
            key_list.insert(2, 'Lot/Serial Number')

        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        writer = csv.DictWriter(fp, fieldnames=key_list)
        writer.writeheader()
        writer.writerows(value_list)
        fp.seek(0)
        p1db_csv = fp.read()
        stock_location_name = stock_inventory.location_id.complete_name
        stock_location_name = str(stock_location_name).replace(" ", "_").replace("/", "-")
        print(stock_location_name)
        reportname = "Inventory_Adjustment-" + stock_location_name
        csvhttpheaders = [('Content-Type', 'text/csv'), ('Content-Disposition', 'attachment;filename=%s.csv;' %reportname), ('Content-Length', len(p1db_csv))]
        response = request.make_response(p1db_csv, headers=csvhttpheaders)
        return response
