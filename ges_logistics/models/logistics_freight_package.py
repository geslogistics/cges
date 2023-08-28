# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class LogisticsFreightPackage(models.Model):
    _name = 'logistics.freight.package'
    _description = 'Freight Packages'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    
    code = fields.Char(string='Code')
    name = fields.Char(string='Name / Size')
    
    is_container = fields.Boolean('Container/Box')
    is_item = fields.Boolean(string='Is Item')
    other = fields.Boolean('Other')
    
    air = fields.Boolean(string='Air')
    ocean = fields.Boolean(string='Ocean')
    road = fields.Boolean(string='Road')
    rail = fields.Boolean(string='Rail')

    desc = fields.Char(string="Description")
    
    unit_type = fields.Selection([('metric','Metric'),('imperial','Imperial')])
    
    metric_height = fields.Float(string='Height (cm)')
    metric_length = fields.Float(string='Length (cm)')
    metric_width = fields.Float(string='Width (cm)')
    metric_volume = fields.Float('Volume (m3)')
    metric_gross_weight = fields.Float('Gross Weight (kg)')

    imperial_height = fields.Float(string='Height (inch)')
    imperial_length = fields.Float(string='Length (inch)')
    imperial_width = fields.Float(string='Width (inch)')
    imperial_volume = fields.Float('Volume (ft3)')
    imperial_gross_weight = fields.Float('Gross Weight (lb)')