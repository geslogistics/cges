from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomsOrder(models.Model):
    
    _name = "logistics.customs.order"
    _description = "Logistics Customs Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    