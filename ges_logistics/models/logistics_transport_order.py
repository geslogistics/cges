from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TransportOrder(models.Model):
    
    _name = "logistics.transport.order"
    _description = "Transportation Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    