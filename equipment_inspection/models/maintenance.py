# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    
    inspection_count = fields.Integer(string="Inspection Count", compute='_compute_maintenance_count')
    maintenance_type_ids = fields.One2many('maintenance.equipment.type', 'equipment_id', string='Maintenance Types')

    @api.one
    def _compute_maintenance_count(self):
        inspection_ids = self.env['equipment.inspection'].search_count([('equipment_id', '=', self.id)])
        self.inspection_count = inspection_ids
        
        
class MaintenanceEquipmentType(models.Model):
    _name = 'maintenance.equipment.type'
    _description = 'Maintenance Types'
    
    maintenance_type_id = fields.Many2one('maintenance.type', 'Type of Maintenance', required=True)
    frequency = fields.Integer('Frequency')
    equipment_id = fields.Many2one('maintenance.equipment', 'Equipment', required=True) 
    

class MaintenanceType(models.Model):
    _name = 'maintenance.type'
    
    name = fields.Char('Type of Maintenance', required=True)
    code = fields.Char('Code', required=True)
    
    
class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    material_ids = fields.One2many('maintenance.request.material', 'maintenance_request_id', string='Maintenance Types')

        
        
class MaintenanceEquipmentType(models.Model):
    _name = 'maintenance.request.material'
    _description = 'Maintenance Materials'
    _rec_name = 'maintenance_request_id'
    
    product_id = fields.Many2one('product.product', 'Product', required=True)
    partner_id = fields.Many2one('res.partner', 'Supplier', domain="[('supplier', '=', True)]")
    qty = fields.Float('Qty', default=1.0)
    cost = fields.Float('Cost')
    cost_total = fields.Float('Total Cost', compute="_calc_product_cost")
    maintenance_request_id = fields.Many2one('maintenance.request', 'Maintenance Request', required=True) 
    
    @api.one
    def _calc_product_cost(self):
        self.cost_total = self.qty * self.cost 
        
    @api.onchange('product_id')
    def _change_product_cost(self):
        if self.product_id:
            self.cost = self.product_id.standard_price
    
    
    
    