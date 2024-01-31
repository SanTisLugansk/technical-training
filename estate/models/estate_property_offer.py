from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'),
                                         ('refused', 'Refused')],
                              copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', reguired=True)
    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)
