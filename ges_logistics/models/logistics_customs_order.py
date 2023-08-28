# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import logging


class CustomsOrder(models.Model):
    _name = "logistics.customs.order"
    _description = "Logistics Customs Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [('bl_awb_number', 'unique (bl_awb_number)',
                         'The BL / AWB Number must be unique, this one is already in the system.')]

    active = fields.Boolean(default=True, string='Active')
    stages = fields.Selection(
        [('draft', 'Draft'), ('pre_bayan', 'Pre Bayan'), ('custom_duty', 'Custom Duty SADAD Paid'),
         ('final', 'Final Bayan'), ('cleared', 'Cleared')], default="draft", tracking=True)
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))

    # Company and Clearance Information
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    date = fields.Date(string="Date", required=True, default=date.today())
    customer_ref = fields.Char(string="Customer Ref", tracking=True)
    company_currency_id = fields.Many2one(comodel_name='res.currency', string="Company Currency",
                                          related='company_id.currency_id')
    shipper_id = fields.Many2one("res.partner", string="Shipper", domain=[('shipper', '=', True)])
    shipper_date = fields.Date(string="By Email DOC Received Date", default=date.today())
    shipment_type = fields.Selection(string="Shipment Type", selection=[('lcl', 'LCL'), ('fcl', 'FCL')], required=False,
                                     tracking=True)

    sadad_no = fields.Char(string="SADAD Number", tracking=True)
    saddad_date = fields.Datetime(string="SADAD Date", tracking=True)
    moved_sadad = fields.Date(string="Moved to SADAD Date", tracking=True)
    sadad_amount = fields.Monetary(string='SADAD Amount', currency_field='company_currency_id', tracking=True)

    bill_types = fields.Selection([('B/L Number', 'B/L Number'), ('Container Wise', 'Container Wise')],
                                  string="Billing Type", tracking=True)
    bl_awb_number = fields.Char(string="BL / AWB Number", tracking=True)

    # Other fields

    vessel_expected_arrival_date = fields.Date(string="Vessel Expected Arrival Date", tracking=True)
    vessel_arrival_date = fields.Date(string="Vessel Arrival Date", tracking=True)
    vessel_discharge_date = fields.Date(string="Vessel Discharge Date", tracking=True)
    vessel_name = fields.Char(string="Vessel Name", tracking=True)

    do_filename = fields.Char(string="Bayan Filename", tracking=True)
    do_attach = fields.Binary(string="DO Attachment", tracking=True)
    do_date = fields.Date(string="DO Date", tracking=True)
    do_num = fields.Char(string="DO Number", tracking=True)

    bayan_attach = fields.Binary(string="Bayan Attachment", tracking=True)
    bayan_filename = fields.Char(string="Bayan", tracking=True)
    fin_bayan_date = fields.Date(string="Final Bayan Date", tracking=True)
    final_attach = fields.Binary(string="Final Bayan Attachment", tracking=True)
    fb_filename = fields.Char(string="Final Bayan Filename", tracking=True)
    bayan_no = fields.Char(string="Bayan No.", tracking=True)
    pre_bayan_date = fields.Date(string="Pre Bayan Date", tracking=True)

    # Additional Information
    remarks = fields.Text(string="Remarks", tracking=True)
    eta = fields.Date(string="ETA", tracking=True)
    etd = fields.Date(string="ETD", tracking=True)
    inspection_date = fields.Date(string="Inspection Date", required=False, tracking=True)
    duty_paid_date = fields.Date(string="Duty Paid Date", required=False, tracking=True)
    gate_pass_date = fields.Date(string="Gate Pass Date", required=False, tracking=True)
    des_Port = fields.Many2one(comodel_name="res.country", string="Discharging Port", required=False, tracking=True)
    lan_Port = fields.Many2one(comodel_name="res.country", string="Landing Port", required=False, tracking=True)

    house_bl = fields.Char(string="House B/L", tracking=True)
    demurrage = fields.Date(string="Demurrage Date", store=True, default=datetime.today(), tracking=True)
    free_time_days = fields.Integer(string="Free Time Days", default='7', tracking=True)
    detention_date = fields.Date(string="Detention Date", store=True)
    port_dues_payment_date = fields.Datetime(string='Port Dues Payment Date')
