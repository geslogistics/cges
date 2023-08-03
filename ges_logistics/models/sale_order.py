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
                self.reference_document = '%s,%s'% ('logistics.storage.order',self.env['logistics.storage.order'].create({}).id)
            elif self.product_template_id.sale_order_line_workflow == 'customs':
                self.reference_document = '%s,%s'% ('logistics.customs.order',self.env['logistics.customs.order'].create({}).id)
            elif self.product_template_id.sale_order_line_workflow == 'service':
                self.reference_document = '%s,%s'% ('logistics.service.order',self.env['logistics.service.order'].create({}).id)
