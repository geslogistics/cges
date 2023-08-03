from odoo import api, fields, models, _

class LogisticsFreightPort(models.Model):
    _name = 'logistics.freight.port'
    _description = 'Logistics Port'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True, string='Active')
    name = fields.Char(string='Name', translate=True, tracking=True)
    code = fields.Char(string='Code', tracking=True)
    air = fields.Boolean(string='Air', tracking=True)
    ocean = fields.Boolean(string='Ocean', tracking=True)
    road = fields.Boolean(string='Road', tracking=True)
    rail = fields.Boolean(string='Rail', tracking=True)
    # Address
    country_id = fields.Many2one('logistics.freight.address.country', string="Country", tracking=True, ondelete='restrict')
    state_id = fields.Many2one('logistics.freight.address.state', string="State", domain="[('country_id', '=', country_id)]", tracking=True, ondelete='restrict')
    city_id = fields.Many2one('logistics.freight.address.city', string="City", domain="[('country_id', '=', country_id),('state_id', '=', state_id)]", tracking=True, ondelete='restrict')
    zip_code = fields.Char(string='Zip Code', tracking=True)
    street = fields.Char(string='Street', tracking=True)
    street2 = fields.Char(string='Street 2', tracking=True)
    street3 = fields.Char(string='Street 3', tracking=True)


    def name_get(self):
        res = []
        for record in self:
            if record.code:
                name = "[" + record.code + "] " + record.name
                res.append((record.id, name))
            else:
                name = record.name
                res.append((record.id, name))
        return res
        return super(LogisticsFreightPort, self).name_get()

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.search(['|','|',('code', operator, name),('name', operator, name),('city_id', operator, name)] + args, limit=limit)
        if not recs.ids:
            return super(LogisticsFreightPort, self).name_search(name=name, args=args, operator=operator,limit=limit)
        return recs.name_get()