# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HRContract(models.Model):
    _inherit = 'hr.contract'

    air_ticket_allowance = fields.Monetary(string='Air Ticket Allowance')


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    # adjust fields

    reference_document = fields.Reference(
        selection=[
            ('logistics.shipment.order', 'Shipment Order'),
            ('logistics.transport.order', 'Transport Order'),
            ('logistics.storage.order', 'Storage Order'),
            ('logistics.customs.order', 'Customs Order'),
            ('logistics.service.order', 'Service Order'),
        ],
        ondelete='restrict', string="Source Document", tracking=True)

    def initiate_reference_document(self):
        # self.reference_document = '%s,%s'% ('logistics.shipment.order',self.env['logistics.shipment.order'].create({}).id)

        if self.product_template_id:
            if self.product_template_id.sale_order_line_workflow == 'shipment':
                newsh = self.env['logistics.shipment.order'].create({})
                self.reference_document = '%s,%s' % ('logistics.shipment.order', newsh.id)
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
                self.reference_document = '%s,%s' % ('logistics.transport.order', newtr.id)
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
                self.reference_document = '%s,%s' % ('logistics.storage.order', newtr.id)
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
                self.reference_document = '%s,%s' % ('logistics.customs.order', newtr.id)
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
                self.reference_document = '%s,%s' % ('logistics.service.order', newtr.id)
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
                self.reference_document = '%s,%s' % ('logistics.transport.order', newtr.id)
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
                self.reference_document = '%s,%s' % ('logistics.storage.order', newtr.id)
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
                self.reference_document = '%s,%s' % ('logistics.customs.order', newtr.id)
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
                self.reference_document = '%s,%s' % ('logistics.service.order', newtr.id)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Service Order',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'logistics.service.order',
                    'res_id': newtr.id,
                    'target': 'current',
                }


class ProductCategory(models.Model):
    _inherit = ['product.category']

    sale_order_line_workflow = fields.Selection([
        ('shipment', 'Shipment'),
        ('transport', 'Transportation'),
        ('service', 'Service'),
        ('storage', 'Storage'),
        ('customs', 'Customs'),
    ], string="Selling Workflow", copy=True, tracking=True)


class Product(models.Model):
    _inherit = ['product.template']

    # adjust fields
    is_logistics = fields.Boolean("Is Logistics")
    product_group_id = fields.Many2one('logistics.product.product.group', string="Product Group")
    freight_type_id = fields.Many2one('logistics.product.freight.type', string="Freight Type",
                                      domain="[('product_group_id','=',product_group_id)]")
    shipment_type_id = fields.Many2one('logistics.product.shipment.type', string="Shipment Type",
                                       domain="[('freight_type_id','=',freight_type_id),('product_group_id','=',product_group_id)]")

    sale_order_line_workflow = fields.Selection([
        ('shipment', 'Shipment'),
        ('transport', 'Transportation'),
        ('service', 'Service'),
        ('storage', 'Storage'),
        ('customs', 'Customs'),
    ], string="Selling Workflow", copy=True, tracking=True)


class ProductGroup(models.Model):
    _name = "logistics.product.product.group"

    name = fields.Char(string="Group Name", required=True, copy=True, tracking=True)
    product_group_category = fields.Selection(
        [('freight', 'Freight'), ('warehousing', 'Warehousing'), ('service', 'Service'), ('others', 'Others')],
        default="freight", string='Product Group Category', required=True, copy=True, tracking=True)


class FreightType(models.Model):
    _name = "logistics.product.freight.type"

    name = fields.Char(string="Freight Type Name", required=True, copy=True, tracking=True)
    freight_type_category = fields.Selection(
        [('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('others', 'Others')],
        default="ocean", string='Freight Type Category', required=True, copy=True, tracking=True)
    product_group_id = fields.Many2one('logistics.product.product.group', string="Product Group")
    # product_group_category = fields.Char('Product Group Category', related="product_group_id.product_group_category")


class ShipmentType(models.Model):
    _name = "logistics.product.shipment.type"

    name = fields.Char(string="Shipment Type Name", required=True, copy=True, tracking=True)
    shipment_type_category = fields.Selection(
        [('full', 'Full Load'), ('less', 'Less Than Load'), ('others', 'Others')],
        default="full", string='Shipment Type Category', required=True, copy=True, tracking=True)
    freight_type_id = fields.Many2one('logistics.product.freight.type', string="Freight Type")
    product_group_id = fields.Many2one('logistics.product.product.group', string="Product Group",
                                       related='freight_type_id.product_group_id')
    # freight_type_category = fields.Char('Freight Type Category', related="freight_type_id.freight_type_category")
