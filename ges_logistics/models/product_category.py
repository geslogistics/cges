from odoo import models, fields, api, _


class ProductCategory(models.Model):
    
    _inherit = ['product.category']

    sale_order_line_workflow = fields.Selection([
        ('shipment', 'Shipment'),
        ('transport', 'Transportation'),
        ('service', 'Service'),
        ('storage', 'Storage'),
        ('customs', 'Customs'),
        ],string="Selling Workflow",copy=True, tracking=True)    
    

    
