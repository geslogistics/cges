# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class LogisticsFreightAddressContinent(models.Model):
    _name = 'logistics.freight.address.continent'
    _description = 'Logistics Continent'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)


class LogisticsFreightAddressRegion(models.Model):
    _name = 'logistics.freight.address.region'
    _description = 'Logistics Region'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    continent_ids = fields.Many2many('logistics.freight.address.continent', 'region_continent', string="Continent(s)",
                                     tracking=True, ondelete='restrict')


class LogisticsFreightAddressCountry(models.Model):
    _name = 'logistics.freight.address.country'
    _description = 'Logistics Country'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code2 = fields.Char(string='ISO Alpha2-Code', tracking=True)
    code = fields.Char(string='ISO Alpha3-Code', tracking=True)
    continent_id = fields.Many2one('logistics.freight.address.continent', string="Continent", tracking=True,
                                   ondelete='restrict')
    region_ids = fields.Many2many('logistics.freight.address.region', 'country_region', string="Region(s)",
                                  tracking=True, ondelete='restrict')
    country_call_code = fields.Integer(string='Country Calling Code', tracking=True)

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = record.name + " [" + record.code + "]"
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightAddressCountry, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', ('code', operator, name), ('name', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightAddressCountry, self).name_search(name=name, args=args, operator=operator,
                                                                           limit=limit)
        return recs.name_get()


class LogisticsFreightAddressState(models.Model):
    _name = 'logistics.freight.address.state'
    _description = 'Logistics State'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    country_id = fields.Many2one('logistics.freight.address.country', string="Country", tracking=True,
                                 ondelete='restrict')

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = record.name + " [" + record.code + "]"
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightAddressState, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', ('code', operator, name), ('name', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightAddressState, self).name_search(name=name, args=args, operator=operator,
                                                                         limit=limit)
        return recs.name_get()


class LogisticsFreightAddressCity(models.Model):
    _name = 'logistics.freight.address.city'
    _description = 'Freight City'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')

    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    country_id = fields.Many2one('logistics.freight.address.country', string="Country", tracking=True,
                                 ondelete='restrict')
    state_id = fields.Many2one('logistics.freight.address.state', string="State",
                               domain="[('country_id', '=', country_id)]", tracking=True, ondelete='restrict')

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = record.name + " [" + record.code + "]"
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightAddressCity, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', ('code', operator, name), ('name', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightAddressCity, self).name_search(name=name, args=args, operator=operator,
                                                                        limit=limit)
        return recs.name_get()


class LogisticsFreightAddress(models.Model):
    _name = 'logistics.freight.address'
    _description = 'Logistics Address'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')

    partner_id = fields.Many2one('res.partner', string="Partner", tracking=True, ondelete='cascade')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    # Address
    country_id = fields.Many2one('logistics.freight.address.country', string="Country", tracking=True,
                                 ondelete='restrict')
    state_id = fields.Many2one('logistics.freight.address.state', string="State",
                               domain="[('country_id', '=', country_id)]", tracking=True, ondelete='restrict')
    city_id = fields.Many2one('logistics.freight.address.city', string="City",
                              domain="[('country_id', '=', country_id),('state_id', '=', state_id)]", tracking=True,
                              ondelete='restrict')
    zip_code = fields.Char(string='Zip Code', tracking=True)
    street = fields.Char(string='Street', tracking=True)
    street2 = fields.Char(string='Street 2', tracking=True)
    street3 = fields.Char(string='Street 3', tracking=True)

    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = record.name + " [" + record.code + "]"
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightAddress, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|', ('code', operator, name), ('name', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightAddress, self).name_search(name=name, args=args, operator=operator,
                                                                    limit=limit)
        return recs.name_get()
