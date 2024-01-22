from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate description"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('0', 'North'),
                                                     ('1', 'East'),
                                                     ('2', 'South'),
                                                     ('3', 'West')])
