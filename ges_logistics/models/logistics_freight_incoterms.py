from odoo import api, fields, models, _

class LogisticsFreightIncoterms(models.Model):
    _name = 'logistics.freight.incoterms'
    _description = 'Freight Incoterms'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    active = fields.Boolean(default=True, string='Active')
    code = fields.Char(string='Code')
    name = fields.Char(string='Name', help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    option_import = fields.Boolean(string="Import")
    option_export = fields.Boolean(string="Export")
    option_ocean = fields.Boolean(string="Ocean")
    option_air = fields.Boolean(string="Air")
    option_rail = fields.Boolean(string="Rail")
    option_road = fields.Boolean(string="Road")
    option_pickup = fields.Boolean(string="Pick-Up")
    option_delivery = fields.Boolean(string="Delivery")
    description = fields.Text(string="Description")
    