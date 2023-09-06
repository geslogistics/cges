# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import logging

_logger = logging.getLogger(__name__)


class CustomsOrder(models.Model):
    _name = "logistics.customs.order"
    _description = "Logistics Customs Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [('bl_number', 'unique (bl_number)', 'The BL Number must be unique, this one is already in the system.'),
                        ('awb_number', 'unique (awb_number)', 'The AWB Number must be unique, this one is already in the system.'),
                        ('lwb_number', 'unique (lwb_number)', 'The LWB Number must be unique, this one is already in the system.')]

    @api.model
    def create(self, vals):
        """
        This method is called when a new record of the CustomsOrder model is created.
        It updates the status of the newly created record based on certain conditions.
        Args:
            - vals: A dictionary containing the field values for the new record.
        Returns:
            - record: The newly created CustomsOrder record.
        """
        record = super().create(vals)
        if not vals.get('status'):
            record._update_status_single()
        return record

    def write(self, vals):
        """
        This method is called when existing records of the CustomsOrder model are updated.
        It updates the status of the records being updated based on certain conditions.
        Args:
            - vals: A dictionary containing the field values to update.
        Returns:
            - res: The result of the write operation.
        """
        if 'status' in vals:
            return super().write(vals)

        res = super().write(vals)

        self._update_status_single()
        return res

    def _update_status_single(self):
        """
        This private method updates the 'status' field of the CustomsOrder record(s)
        based on the values of various date fields and the 'direction' field.
        It checks conditions for both 'import' and 'export' directions and sets the
        appropriate 'status' value if the condition is met.
        """
        """Update status on current record only"""
        self.ensure_one()
        if self.direction == 'import':
            # Check and update status for 'import' direction
            if self.shipment_doc_received_date and self.status != 'docs_received':
                self.status = 'docs_received'
            elif self.vessel_expected_arrival_date and self.status != 'pending_vessel_arrival':
                self.status = 'pending_vessel_arrival'
            elif self.vessel_discharge_date and self.status != 'cargo_discharged_pending_bayan_print':
                self.status = 'cargo_discharged_pending_bayan_print'
            elif self.pre_customs_dec_date and self.status != 'pre_bayan_printed':
                self.status = 'pre_bayan_printed'
            elif self.customs_duty_payment_notification_date and self.status != 'shipment_cleared_pending_duty_payment':
                self.status = 'shipment_cleared_pending_duty_payment'
            elif self.customs_duty_payment_date and self.status != 'custom_duty_paid':
                self.status = 'custom_duty_paid'
            elif self.loading_card_date and self.status != 'shipment_ready_for_pullout':
                self.status = 'shipment_ready_for_pullout'
        elif self.direction == 'export':
            # Check and update status for 'export' direction
            if self.shipment_doc_received_date and self.status != 'docs_received':
                self.status = 'docs_received'
            elif self.vessel_expected_arrival_date and self.status != 'pending_vessel_arrival':
                self.status = 'pending_vessel_arrival'
            elif self.manifest_date and self.status != 'cargo_discharged_pending_bayan_print':
                self.status = 'cargo_discharged_pending_bayan_print'
            elif self.pre_customs_dec_date and self.status != 'pre_bayan_printed':
                self.status = 'pre_bayan_printed'
            elif self.broker_transportation_order_date and self.status != 'transport_order_created_awaiting_port_shuttling':
                self.status = 'transport_order_created_awaiting_port_shuttling'
            elif self.shipment_in_port_date and self.status != 'shipment_inside_port':
                self.status = 'shipment_inside_port'
            elif self.ok_to_load_date and self.status != 'shipment_ready_to_load_in_vessel':
                self.status = 'shipment_ready_to_load_in_vessel'

    @api.onchange('direction', 'partner_id')
    def _onchange_direction_partner_id(self):
        if self.direction == 'export':
            self.shipper_id = self.partner_id
            self.consignee_id = False
        elif self.direction == 'import':
            self.consignee_id = self.partner_id
            self.shipper_id = False
        else:
            self.shipper_id = self.consignee_id = False

    @api.depends('customs_duty_payment_date', 'vessel_discharge_date')
    def _compute_clearance_time_taken(self):
        for record in self:
            if record.customs_duty_payment_date and record.vessel_discharge_date:
                delta = record.customs_duty_payment_date - record.vessel_discharge_date
                record.clearance_time_taken = delta.days
            else:
                record.clearance_time_taken = 0

    @api.constrains('clearance_time_taken', 'clearance_delay_reason')
    def _check_clearance_delay_reason(self):
        for record in self:
            if record.clearance_time_taken >= 3:
                if not record.clearance_delay_reason or len(record.clearance_delay_reason.strip()) < 15:
                    raise ValidationError("Clearance Delay Reason must be at least 15 characters when Clearance Time Taken is 3 days or more.")

    active = fields.Boolean(default=True, string='Active')
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    company_currency_id = fields.Many2one(comodel_name='res.currency', string="Company Currency", related='company_id.currency_id')
    state = fields.Selection([('draft', 'Draft'), ('docs_received', 'Docs Received'), ('pre_clearance', 'Pre Clearance'), ('clearance', 'Clearance'),
                              ('post_clearance', 'Post Clearance')], default='draft', string='State', tracking=True)
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))

    # Customs Shipment Details
    transport = fields.Selection(([('ocean', 'Ocean'), ('air', 'Air'), ('road', 'Road'), ('rail', 'Rail')]), string='Transport Via', required=True,
                                 tracking=True)
    direction = fields.Selection(string="Direction", selection=[('import', 'Import'), ('export', 'Export')], required=True, tracking=True)
    shipment_type_id = fields.Many2one(comodel_name='logistics.product.shipment.type', string='Shipment Type', required=True, tracking=True)
    commodity_type = fields.Selection(string="Commodity Type", selection=[('general_cargo', 'General Cargo'), ('dangerous_goods', 'Dangerous Goods'),
                                                                          ('temperature_controlled', 'Temperature Controlled'),
                                                                          ('delicate_high_value', 'Delicate High Value'), ('roro', 'RoRo'),
                                                                          ('livestock', 'Livestock')], required=True, tracking=True)
    commercial_invoice = fields.Binary(string='Commercial Invoice', tracking=True)
    commercial_invoice_file_name = fields.Char(string='Commercial Invoice File Name', tracking=True)
    bl_number = fields.Char(string="BL Number", tracking=True)
    awb_number = fields.Char(string="AWB Number", tracking=True)
    lwb_number = fields.Char(string="LWB Number", tracking=True)

    # Customer Details
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    customer_reference = fields.Char(string="Customer Reference", tracking=True)
    # customer_reference_type_id = fields.Many2one(comodel_name='logistics.customer.reference.type', string="Customer Reference Type", tracking=True)
    billing_type = fields.Selection([('B/L Number', 'B/L Number'), ('Container Wise', 'Container Wise')], string="Billing Type", tracking=True)

    # Shipment Details
    shipper_id = fields.Many2one("res.partner", string="Shipper", domain=[('shipper', '=', True)], tracking=True)
    consignee_id = fields.Many2one("res.partner", string="Consignee", domain=[('consignee', '=', True)], tracking=True)
    shipment_doc_received_date = fields.Date(string='Shipment Documents Received from Customer', tracking=True)
    broker_id = fields.Many2one(comodel_name='res.partner', string='Broker', domain=[('consignee', '=', True)], tracking=True)
    discharging_port_id = fields.Many2one(comodel_name='logistics.freight.port', string='Discharging Port', tracking=True)
    landing_port_id = fields.Many2one(comodel_name='logistics.freight.port', string='Landing Port', tracking=True)
    status = fields.Selection(
        [('draft', 'Draft'), ('awaiting_shipment_docs', 'Awaiting Shipment Docs'), ('docs_received', 'Docs Received'),
         ('pending_vessel_arrival', 'Pending Vessel Arrival'), ('cargo_discharged_pending_bayan_print', 'Cargo Discharged - Pending Bayan Print'),
         ('pre_bayan_printed', 'Pre Bayan Printed'), ('shipment_cleared_pending_duty_payment', 'Shipment Cleared - Pending Duty Payment'),
         ('custom_duty_paid', 'Custom Duty Paid'), ('shipment_ready_for_pullout', 'Shipment Ready for PullOut'),
         ('transport_order_created_awaiting_port_shuttling', 'Transport Order Created - Awaiting Port Shuttling'),
         ('shipment_inside_port', 'Shipment Inside Port'), ('shipment_ready_to_load_in_vessel', 'Shipment Ready To Load in Vessel')], default="draft",
        tracking=True)

    # Vessel Information
    vessel_name = fields.Char(string='Vessel Name', tracking=True)
    vessel_expected_arrival_date = fields.Date(string='Vessel Expected Arrival Date', tracking=True)
    vessel_arrival_date = fields.Date(string='Vessel Arrival Date', tracking=True)
    manifest_date = fields.Date(string='Manifest Date', tracking=True)
    vessel_discharge_date = fields.Date(string='Vessel Discharge Date', tracking=True)

    # Clearance Stage
    pre_customs_dec_no = fields.Char(string='Pre-Customs Declaration Number', tracking=True)
    pre_customs_dec_date = fields.Date(string='Pre-Customs Declaration Date', tracking=True)
    pre_customs_dec_attachment = fields.Binary(string='Pre-Customs Declaration Attachment', tracking=True)
    pre_customs_dec_attachment_filename = fields.Char(string='Pre-Customs Declaration Attachment', tracking=True)
    customs_duty_payment_notification_date = fields.Date(string='Custom Duty Payment Notification Date', tracking=True)
    customs_duty_payment_reference_number = fields.Char(string='Custom Duty Payment Reference Number', tracking=True)
    customs_duty_payment_amount = fields.Monetary(string='Custom Duty Payment Amount', currency_field='company_currency_id', tracking=True)
    customs_duty_payment_date = fields.Date(string='Custom Duty Payment Date', tracking=True)
    final_customs_declaration_date = fields.Date(string='Final Customs Declaration Date', tracking=True)
    final_customs_clearance_attachment = fields.Binary(string='Final Customs Declaration Attachment', tracking=True)
    final_customs_clearance_attachment_filename = fields.Char(string='Final Customs Declaration Attachment', tracking=True)
    broker_transportation_order_date = fields.Date(string='Broker Transportation Order Date', tracking=True)

    # Post Clearance Stage
    do_number = fields.Char(string='Delivery Order Number', tracking=True)
    do_collection_date = fields.Date(string='Delivery Order Collection Date', tracking=True)
    do_attachment = fields.Binary(string='Delivery Order Attachment', tracking=True)
    do_attachment_file_name = fields.Char(string='Delivery Order Attachment File Name', tracking=True)
    loading_card_date = fields.Date(string='Loading Card Date', tracking=True)
    pd_ce_payment_date = fields.Date(string='Port Dues and Customs Examination Payment Date', tracking=True)
    shipment_in_port_date = fields.Date(string='Shipment In Port Date', tracking=True)
    ok_to_load_date = fields.Date(string='OK To Load Date', tracking=True)

    # Demurrage and Detention Details
    demurrage_date = fields.Date(string='Demurrage Date', tracking=True)
    free_time_days = fields.Integer(string='Free Time Days', tracking=True, default=7)
    detention_date = fields.Date(string='Detention Date', tracking=True)

    # Additional Customs Information
    inspection_date = fields.Date(string='Inspection Date', tracking=True)
    duty_paid_date = fields.Date(string='Duty paid Date', tracking=True)
    gate_pass_date = fields.Date(string='Gate Pass Date', tracking=True)
    pd_payment_date = fields.Date(string='Port Dues Payment Date', tracking=True)
    remarks = fields.Text(string="Remarks", tracking=True)
    clearance_time_taken = fields.Integer(string='Clearance Time Taken', tracking=True, compute='_compute_clearance_time_taken', store=True)
    clearance_delay_reason = fields.Text(string='Clearance Delay Reason', tracking=True)

    # One2Many Fields
    freight_package_ids = fields.One2many('shipment.package.line', 'customs_id')


class ShipmentPackageLine(models.Model):
    _inherit = 'shipment.package.line'

    customs_id = fields.Many2one('logistics.customs.order', string='Customs Order')
