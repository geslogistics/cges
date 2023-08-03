from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ServiceOrder(models.Model):
    
    _name = "logistics.service.order"
    _description = "Service Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', copy=False, default=lambda self: ('New'))
    