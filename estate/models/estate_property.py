from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate description"

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available from',
                                    copy=False,
                                    default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden area (sqm)')
    garden_orientation = fields.Selection(selection=[('0', 'North'),
                                                     ('1', 'East'),
                                                     ('2', 'South'),
                                                     ('3', 'West')])
    state = fields.Selection(selection=[('new', 'New'),
                                        ('offer_received', 'Offer received'),
                                        ('offer_accepted', 'Offer accepted'),
                                        ('sold','Sold'),
                                        ('canceled','Canceled')],
                             default='new', required=True, string='Status', copy=False)
    active = fields.Boolean(default=True)
    is_available = fields.Boolean(compute='_compute_is_available')

    def _compute_is_available(self):
        if self.date_availability==False:
            self.available = False
        else:
            self.available = (self.date_availability<=fields.Date.today())
