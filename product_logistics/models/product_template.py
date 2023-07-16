from odoo import models, fields, api, _


class Product(models.Model):
    
    _inherit = ['product.template']

    #adjust fields
    is_logistics = fields.Boolean("Is Logistics")
    product_group_id = fields.Many2one('logistics.product.group', string="Product Group")
    freight_type_id = fields.Many2one('logistics.freight.type', string="Freight Type", domain="[('product_group_id','=',product_group_id)]")
    shipment_type_id = fields.Many2one('logistics.shipment.type', string="Shipment Type", domain="[('freight_type_id','=',freight_type_id),('product_group_id','=',product_group_id)]")
    
    
    

    


class ProductGroup(models.Model):
    
    _name = "logistics.product.group"

    name = fields.Char(string="Group Name", required=True, copy=True, tracking=True)
    product_group_category = fields.Selection(
        [('freight', 'Freight'), ('warehousing', 'Warehousing'), ('service', 'Service'),('others','Others')],
        default="freight", string='Product Group Category', required=True, copy=True, tracking=True)

class FreightType(models.Model):
    
    _name = "logistics.freight.type"

    name = fields.Char(string="Freight Type Name", required=True, copy=True, tracking=True)
    freight_type_category = fields.Selection(
        [('ocean', 'Ocean'), ('air', 'Air'), ('land', 'Land'),('rail','Rail'),('others','Others')],
        default="ocean", string='Freight Type Category', required=True, copy=True, tracking=True)
    product_group_id = fields.Many2one('logistics.product.group', string="Product Group")
    #product_group_category = fields.Char('Product Group Category', related="product_group_id.product_group_category")

class ShipmentType(models.Model):
    
    _name = "logistics.shipment.type"

    name = fields.Char(string="Shipment Type Name", required=True, copy=True, tracking=True)
    shipment_type_category = fields.Selection(
        [('full', 'Full Load'), ('less', 'Less Than Load'),('others','Others')],
        default="full", string='Shipment Type Category', required=True, copy=True, tracking=True)
    freight_type_id = fields.Many2one('logistics.freight.type', string="Freight Type")
    product_group_id = fields.Many2one('logistics.product.group', string="Product Group", related='freight_type_id.product_group_id')
    #freight_type_category = fields.Char('Freight Type Category', related="freight_type_id.freight_type_category")
    