from odoo import models, fields, api, _


class SaleOrderLine(models.Model):
    
    _inherit = ['sale.order.line']

    #adjust fields

    reference_document = fields.Reference (
        selection = [
            ('logistics.shipment.order', 'Shipment Order'),
            ('logistics.transport.order', 'Transport Order'),
            ('logistics.storage.order', 'Storage Order'),
            ('logistics.customs.order', 'Customs Order'),
            ('logistics.service.order', 'Service Order'),
            ],
        ondelete='restrict', string = "Source Document", tracking=True)  

    def initiate_reference_document(self):
        #self.reference_document = '%s,%s'% ('logistics.shipment.order',self.env['logistics.shipment.order'].create({}).id)


        if self.product_template_id:
            if self.product_template_id.sale_order_line_workflow == 'shipment':
                newsh = self.env['logistics.shipment.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.shipment.order',newsh.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Shipment Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.shipment.order',
                'res_id': newsh.id,
                'target': 'current',
                }
                
            elif self.product_template_id.sale_order_line_workflow == 'transport':
                
                newtr = self.env['logistics.transport.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.transport.order',newtr.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Transport Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.transport.order',
                'res_id': newtr.id,
                'target': 'current',
                }
            
            elif self.product_template_id.sale_order_line_workflow == 'storage':
                
                newtr = self.env['logistics.storage.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.storage.order',newtr.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Storage Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.storage.order',
                'res_id': newtr.id,
                'target': 'current',
                }
            
            elif self.product_template_id.sale_order_line_workflow == 'customs':
                
                newtr = self.env['logistics.customs.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.customs.order',newtr.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Customs Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.customs.order',
                'res_id': newtr.id,
                'target': 'current',
                }
            
            elif self.product_template_id.sale_order_line_workflow == 'service':
                
                newtr = self.env['logistics.service.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.service.order',newtr.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Service Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.service.order',
                'res_id': newtr.id,
                'target': 'current',
                }
            
    def select_reference_document(self):
        if self.product_template_id:
            if self.product_template_id.sale_order_line_workflow == 'shipment':
                return {
                'type': 'ir.actions.act_window',
                'name': 'Shipment Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.shipment.order',
                'res_id': newsh.id,
                'target': 'current',
                }
                
            elif self.product_template_id.sale_order_line_workflow == 'transport':
                
                newtr = self.env['logistics.transport.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.transport.order',newtr.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Transport Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.transport.order',
                'res_id': newtr.id,
                'target': 'current',
                }
            
            elif self.product_template_id.sale_order_line_workflow == 'storage':
                
                newtr = self.env['logistics.storage.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.storage.order',newtr.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Storage Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.storage.order',
                'res_id': newtr.id,
                'target': 'current',
                }
            
            elif self.product_template_id.sale_order_line_workflow == 'customs':
                
                newtr = self.env['logistics.customs.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.customs.order',newtr.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Customs Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.customs.order',
                'res_id': newtr.id,
                'target': 'current',
                }
            
            elif self.product_template_id.sale_order_line_workflow == 'service':
                
                newtr = self.env['logistics.service.order'].create({})
                self.reference_document = '%s,%s'% ('logistics.service.order',newtr.id)
                return {
                'type': 'ir.actions.act_window',
                'name': 'Service Order', 
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'logistics.service.order',
                'res_id': newtr.id,
                'target': 'current',
                }

    