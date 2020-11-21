# -*- coding: utf-8 -*-
# Copyright (c) 2015-Present TidyWay Software Solution. (<https://tidyway.in/>)

import pytz
import time

from operator import itemgetter
from itertools import groupby

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from _datetime import date


class StockValuationCategory(models.AbstractModel):
    _name = 'report.stock_valuation_on_date.stock_valuation_ondate_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        self.begining_qty = 0.0
        self.total_in = 0.0
        self.total_out = 0.0
        self.total_int = 0.0
        self.total_adj = 0.0
        self.total_begin = 0.0
        self.total_end = 0.0
        self.global_subtotal_cost = 0.0
        self.total_inventory = []
        self.value_exist = {}
        return {
            'doc_ids': self._ids,
            'docs': self,
            'data': data,
            'time': time,
            'get_warehouse_name': self.get_warehouse_name,
            'get_warehouses_block': self._get_warehouses_block,
            'get_company': self._get_company,
            'get_product_name': self._product_name,
            'get_product_uom': self._product_uom,
            'get_categ': self._get_categ,
            'get_lines': self._get_lines,
            'get_beginning_inventory': self._get_beginning_inventory,
            'get_ending_inventory': self._get_ending_inventory,
            'get_value_exist': self._get_value_exist,
            'total_in': self._total_in,
            'total_out': self._total_out,
            'total_int': self._total_int,
            'total_adj': self._total_adj,
            'total_begin': self._total_begin,
            'total_vals': self._total_vals,
            'total_end': self._total_end,
            'get_cost': self._get_cost,
            'get_subtotal_cost': self._get_subtotal_cost,
            'categ_subtotal_cost': self._categ_subtotal_cost,
            'get_filter_assets':self.get_filter_assets
            }

    def _total_in(self):
        """
        category wise inward Qty
        """
        return self.total_in

    def _total_out(self):
        """
        category wise out Qty
        """
        return self.total_out

    def _total_int(self):
        """
        category wise internal Qty
        """
        return self.total_int

    def _total_adj(self):
        """
        category wise adjustment Qty
        """
        return self.total_adj

    def _total_begin(self):
        """
        category wise begining Qty
        """
        return self.total_begin

    def _total_end(self):
        """
        category wise ending Qty
        """
        return self.total_end

    def _categ_subtotal_cost(self):
        """
        category wise subtotal
        """
        return self.global_subtotal_cost

    def _total_vals(self, company_id):
        """
        Grand Total Inventory
        """
        ftotal_in = ftotal_out = ftotal_int = ftotal_adj \
            = ftotal_begin = ftotal_end = fsubtotal_cost = 0.0
        for data in self.total_inventory:
            for key, value in data.items():
                if key[1] == company_id:
                    ftotal_in += value['total_in']
                    ftotal_out += value['total_out']
                    ftotal_int += value['total_int']
                    ftotal_adj += value['total_adj']
                    ftotal_begin += value['total_begin']
                    ftotal_end += value['total_end']
                    fsubtotal_cost += value['total_subtotal']

        return ftotal_begin, ftotal_in, ftotal_out, ftotal_int, ftotal_adj, ftotal_end, fsubtotal_cost

    def _get_warehouses_block(self, warehouse_ids, company_id):
        warehouse_obj = self.env['stock.warehouse']
        warehouses = 'ALL'
        if warehouse_ids:
            warehouse_rec = warehouse_obj.search([
                                  ('id', 'in', warehouse_ids),
                                  ('company_id', '=', company_id)
                                  ])
            if warehouse_rec:
                warehouses = ",".join([x.name for x in warehouse_rec])
            else:
                warehouses = '-'
        return warehouses

    def _get_value_exist(self, categ_id, company_id):
        """
        Compute Total Values
        """
        total_in = total_out = total_int \
            = total_adj = total_begin = subtotal_cost = 0.0
        for warehouse in self.value_exist[categ_id]:
            total_in += warehouse.get('product_qty_in', 0.0)
            total_out += warehouse.get('product_qty_out', 0.0)
            total_int += warehouse.get('product_qty_internal', 0.0)
            total_adj += warehouse.get('product_qty_adjustment', 0.0)
            total_begin += warehouse.get('begining_qty', 0.0)
            subtotal_cost += warehouse.get('subtotal_cost', 0.0)

        self.total_in = total_in
        self.total_out = total_out
        self.total_int = total_int
        self.total_adj = total_adj
        self.total_begin = total_begin
        self.total_end = total_begin + total_in + total_out + total_int + total_adj
        self.global_subtotal_cost = subtotal_cost
        self.total_inventory.append({
                                     (categ_id, company_id):{
                                                            'total_in': total_in,
                                                            'total_out': total_out,
                                                            'total_int': total_int,
                                                            'total_adj': total_adj,
                                                            'total_begin': total_begin,
                                                            'total_end': total_begin + total_in + total_out + total_int + total_adj,
                                                            'total_subtotal': subtotal_cost
                                                            }})
        return ''

    def _get_company(self, company_ids):
        res_company_pool = self.env['res.company']
        if not company_ids:
            company_ids = [x.id for x in res_company_pool.search([])]

        # filter to only have warehouses.
        selected_companies = []
        for company_id in company_ids:
            if self.env['stock.warehouse'].search([('company_id', '=', company_id)]):
                selected_companies.append(company_id)

        return res_company_pool.browse(selected_companies).read(['name', 'currency_id'])
    
    def get_filter_assets(self, filter_assets):
        product_assets_pool = self.env['product.template']
        if not assets_ids:
            assets_ids = [x.id for x in product_assets.search([])]

        # filter to only have warehouses.
        selected_assets = []
        for assets in assets_ids:
            if self.env['product.template'].search([('is_an_asset', '=', True)]):
                selected_assets.append(assets)

        return product_assets_pool.browse(selected_assets).read(['name', 'currency_id'])

    def get_warehouse_name(self, warehouse_ids):
        """
        Return warehouse names
            - WH A, WH B...
        """
        warehouse_obj = self.env['stock.warehouse']
        if not warehouse_ids:
            warehouse_ids = [x.id for x in warehouse_obj.search([])]
        war_detail = warehouse_obj.read(warehouse_ids, ['name'])
        return ', '.join([lt['name'] or '' for lt in war_detail])
    
    def _get_beginning_inventory(self, data, company_id, product_id, current_record):
        """
        Process:
            -Pass locations , start date and product_id
        Return:
            - Beginning inventory of product for exact date
        """

        # find all warehouses and get data for that product
        warehouse_ids = data['form'] and data['form'].get('warehouse_ids', []) or []
        if not warehouse_ids:
            warehouse_ids = self.find_warehouses(company_id)
        # find all locations from all warehouse for that company

        location_id = data['form'] and data['form'].get('location_id') or False
        if location_id:
            locations = [location_id]
        else:
            locations = self._find_locations(warehouse_ids)
        
        filter_assets = data['form'] and data['form'].get('filter_assets') or False
        if filter_assets:
            assets = self.find_assets(filter_assets)
        else:
            assets = self.find_not_assets(filter_assets)
            
        
        from_date = self.convert_withtimezone(data['form']['start_date'] + ' 00:00:00')
        self._cr.execute(''' 
                        SELECT id,coalesce(sum(qty), 0.0) as qty
                        FROM
                            ((
                            SELECT
                                pp.id, pp.default_code,m.date,
                                coalesce(sum(-m.product_qty)::decimal, 0.0) AS qty
                            FROM product_product pp 
                            LEFT JOIN stock_move m ON (m.product_id=pp.id)
                            LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                            LEFT JOIN stock_location l ON (m.location_id=l.id)    
                            LEFT JOIN stock_picking p ON (m.picking_id=p.id)

                            WHERE m.date <  %s AND (m.location_id in %s) AND (m.location_dest_id not in %s)
                             AND m.state='done' AND pp.active=True AND pp.id = %s AND (pt.id in %s)
                            GROUP BY  pp.id, pp.default_code,m.date
                            ) 
                            UNION ALL
                            (
                            SELECT
                                pp.id, pp.default_code,m.date,
                                coalesce(sum(m.product_qty)::decimal, 0.0) AS qty
                            FROM product_product pp 
                            LEFT JOIN stock_move m ON (m.product_id=pp.id)
                            LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                            LEFT JOIN stock_location l ON (m.location_dest_id=l.id)    
                            LEFT JOIN stock_picking p ON (m.picking_id=p.id)
                            WHERE m.date <  %s AND (m.location_dest_id in %s) AND (m.location_id not in %s)
                             AND m.state='done' AND pp.active=True AND pp.id = %s AND (pt.id in %s)
                             
                            GROUP BY  pp.id,pp.default_code,m.date
                            ))
                        AS foo
                        GROUP BY id
                    ''', (from_date, tuple(locations), tuple(locations), product_id, tuple(assets), from_date, tuple(locations), tuple(locations), product_id, tuple(assets)))

        res = self._cr.dictfetchall()
        self.begining_qty = res and res[0].get('qty', 0.0) or 0.0

        current_record.update({'begining_qty': res and res[0].get('qty', 0.0) or 0.0})
        return self.begining_qty

    def _get_ending_inventory(self, in_qty, out_qty, internal_qty, adjust_qty):
        """
        Process:
            -Inward, outward, internal, adjustment
        Return:
            - total of those qty
        """
        return self.begining_qty + in_qty + out_qty + internal_qty + adjust_qty

    def _get_cost(self, company_id, product_id, inventory_date):
        """
        Return:
            - inventory cost on  date
            - Working only for average and standard cost
        """
        #inventory_date = self.convert_withtimezone(inventory_date + ' 00:00:00')
        if isinstance(inventory_date, date):
            inventory_date = inventory_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        inventory_date = datetime.strptime(inventory_date, DEFAULT_SERVER_DATE_FORMAT)
        inventory_date = fields.Datetime.to_string(
                   inventory_date.replace(hour=23, minute=59, second=59))
        company_args = []
        if company_id:
            company_args = [('company_id', 'in', [company_id, False])]
        history = self.env['product.price.history'].search(company_args + [
            ('product_id', '=', product_id),
            ('create_date', '<=', inventory_date or fields.Datetime.now())],
           limit=1, order="id desc")
        cost_value = history.cost or 0.0
        if not cost_value:
            move = self.env['stock.move'].search(company_args+[
                ('product_id', '=', product_id),
                ('purchase_line_id', '!=', False),
                ('state', '=', 'done'),
                ('date', '<=', inventory_date and fields.Datetime.now())],
               limit=1, order="id desc")
            cost_value = move.purchase_line_id.price_unit or 0.0
        return cost_value and round(cost_value, 2) or 0.0

    def _get_subtotal_cost(self, cost, ending_inv, current_record):
        subtotal_cost = cost and ending_inv and round((cost * ending_inv), 2) or 0.0
        current_record.update({'subtotal_cost': subtotal_cost})
        return subtotal_cost

    # Report totally depends on picking type, need to check in deeply when directly move created from anywhere.
    def category_wise_value(self, start_date, end_date, locations, filter_product_categ_ids=[], assets=[]):
        """
        Complete data with category wise
            - In Qty (Inward Quantity to given location)
            - Out Qty(Outward Quantity to given location)
            - Internal Qty(Internal Movements(or null movements) to given location: out/in both : out must be - ,In must be + )
            - Adjustment Qty(Inventory Loss movements to given location: out/in both: out must be - ,In must be + )
        Return:
            [{},{},{}...]
        """
            
        self._cr.execute('''
                        SELECT pp.id AS product_id,pt.categ_id,
                            sum((
                            CASE WHEN spt.code in ('outgoing') AND sm.location_id in %s AND sourcel.usage !='inventory' AND destl.usage !='inventory' 
                            THEN -(sm.product_qty) 
                            ELSE 0.0 
                            END
                            )) AS product_qty_out,
                            sum((
                            CASE WHEN spt.code in ('incoming') AND sm.location_dest_id in %s AND sourcel.usage !='inventory' AND destl.usage !='inventory' 
                            THEN (sm.product_qty) 
                            ELSE 0.0 
                            END
                            )) AS product_qty_in,
                        
                            sum((
                            CASE WHEN (spt.code ='internal' OR spt.code is null) AND sm.location_dest_id in %s AND sm.location_id not in %s AND sourcel.usage !='inventory' AND destl.usage !='inventory' 
                            THEN (sm.product_qty)  
                            WHEN (spt.code ='internal' OR spt.code is null) AND sm.location_id in %s AND sm.location_dest_id not in %s AND sourcel.usage !='inventory' AND destl.usage !='inventory' 
                            THEN -(sm.product_qty) 
                            ELSE 0.0 
                            END
                            )) AS product_qty_internal,
                        
                            sum((
                            CASE WHEN sourcel.usage = 'inventory' AND sm.location_dest_id in %s  
                            THEN  (sm.product_qty)
                            WHEN destl.usage ='inventory' AND sm.location_id in %s 
                            THEN -(sm.product_qty)
                            ELSE 0.0 
                            END
                            )) AS product_qty_adjustment
                        
                        FROM product_product pp 
                        LEFT JOIN  stock_move sm ON (sm.product_id = pp.id and sm.date >= %s and sm.date <= %s and sm.state = 'done' and sm.location_id != sm.location_dest_id)
                        LEFT JOIN stock_picking sp ON (sm.picking_id=sp.id)
                        LEFT JOIN stock_picking_type spt ON (spt.id=sp.picking_type_id)
                        LEFT JOIN stock_location sourcel ON (sm.location_id=sourcel.id)
                        LEFT JOIN stock_location destl ON (sm.location_dest_id=destl.id)
                        LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                        WHERE pt.type!='consu' AND (pt.id in %s)
                        GROUP BY pt.categ_id, pp.id order by pt.categ_id

                        ''', (tuple(locations), tuple(locations), tuple(locations), tuple(locations), tuple(locations), tuple(locations), tuple(locations), tuple(locations), start_date, end_date, tuple(assets)))

        values = self._cr.dictfetchall()

        for none_to_update in values:
            if not none_to_update.get('product_qty_out'):
                none_to_update.update({'product_qty_out':0.0})
            if not none_to_update.get('product_qty_in'):
                none_to_update.update({'product_qty_in':0.0})

        # filter by categories
        if filter_product_categ_ids:
            values = self._remove_product_cate_ids(values, filter_product_categ_ids)
        return values

    def _remove_zero_inventory(self, values):
        final_values = []
        for rm_zero in values:
            if rm_zero['product_qty_in'] == 0.0 and rm_zero['product_qty_internal'] == 0.0 and rm_zero['product_qty_out'] == 0.0 and rm_zero['product_qty_adjustment'] == 0.0:
                pass
            else: final_values.append(rm_zero)
        return final_values

    def _remove_product_cate_ids(self, values, filter_product_categ_ids):
        final_values = []
        for rm_products in values:
            if rm_products['categ_id'] not in filter_product_categ_ids:
                pass
            else: final_values.append(rm_products)
        return final_values

    def _get_categ(self, categ):
        """
        Find category name with id
        """
        return self.env['product.category'].browse(categ).read(['name'])[0]['name']

    def _product_name(self, product_id):
        """
        Find product name and assign to it
        """
        product = self.env['product.product'].browse(product_id).name_get()
        return product and product[0] and product[0][1] or ''

    def _product_uom(self, product_id):

        product = self.env['product.product'].browse(product_id)
        return product.uom_id.name or ''

    def find_warehouses(self, company_id):
        """
        Find all warehouses
        """
        return [x.id for x in self.env['stock.warehouse'].search([('company_id', '=', company_id)])]
    
    def find_assets(self, filter_assets):
        """
        Find all assets
        """
        return [x.id for x in self.env['product.template'].search([('is_an_asset', '=', True),('type', '!=', 'consu')])]
    
    def find_not_assets(self, filter_assets):
        """
        Find all product that are not assets
        """
        return [x.id for x in self.env['product.template'].search([('is_an_asset', '!=', True),('type', '!=', 'consu')])]
        
    def _find_locations(self, warehouses):
        """
            Find all warehouses stock locations and its childs.
        """
        warehouse_obj = self.env['stock.warehouse']
        location_obj = self.env['stock.location']
        stock_ids = []
        for warehouse in warehouses:
            stock_ids.append(warehouse_obj.sudo().browse(warehouse).view_location_id.id)
        # stock_ids = [x['view_location_id'] and x['view_location_id'][0] for x in warehouse_obj.sudo().read(self.cr, 1, warehouses, ['view_location_id'])]
        return [l.id for l in location_obj.search([('location_id', 'child_of', stock_ids)])]

    def convert_withtimezone(self, userdate):
        """ 
            Convert to Time-Zone with compare to UTC
        """
        user_date = datetime.strptime(userdate, DEFAULT_SERVER_DATETIME_FORMAT)
        tz_name = self.env.context.get('tz') or self.env.user.tz
        if tz_name:
            utc = pytz.timezone('UTC')
            context_tz = pytz.timezone(tz_name)
            # not need if you give default datetime into entry ;)
            user_datetime = user_date  # + relativedelta(hours=24.0)
            local_timestamp = context_tz.localize(user_datetime, is_dst=False)
            user_datetime = local_timestamp.astimezone(utc)
            return user_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return user_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _get_lines(self, data, company):
        """
        Process:
            Pass start date, end date, locations to get data from moves,
            Merge those data with locations,
        Return:
            {category : [{},{},{}...], category : [{},{},{}...],...}
        """

        start_date = self.convert_withtimezone(data['form']['start_date'] + ' 00:00:00')
        end_date = self.convert_withtimezone(data['form']['end_date'] + ' 23:59:59')
        warehouse_ids = data['form'] and data['form'].get('warehouse_ids', []) or []
        filter_product_categ_ids = data['form'] and data['form'].get('filter_product_categ_ids') or []
        if not warehouse_ids:
            warehouse_ids = self.find_warehouses(company)

        # find all locations from all warehouse for that company
        location_id = data['form'] and data['form'].get('location_id') or False
        if location_id:
            locations = [location_id]
        else:
            locations = self._find_locations(warehouse_ids)
        
        
        filter_assets = data['form'] and data['form'].get('filter_assets') or False
        if filter_assets:
            assets = self.find_assets(filter_assets)
        else:
            assets = self.find_not_assets(filter_assets)
            

        # get data from all warehouses.
        records = self.category_wise_value(start_date, end_date, locations, filter_product_categ_ids, assets)

        # records by categories
        sort_by_categories = sorted(records, key=itemgetter('categ_id'))
        records_by_categories = dict((k, [v for v in itr]) for k, itr in groupby(sort_by_categories, itemgetter('categ_id')))

        self.value_exist = records_by_categories
        return records_by_categories

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
