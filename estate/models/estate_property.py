from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate description"
    _order = "id desc"

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string='Available from',
                                    copy=False,
                                    default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden area (sqm)')
    garden_orientation = fields.Selection(selection=[('north', 'North'),
                                                     ('east', 'East'),
                                                     ('south', 'South'),
                                                     ('west', 'West')],
                                          # copy=False
                                          )
    state = fields.Selection(selection=[('new', 'New'),
                                        ('offer_received', 'Offer received'),
                                        ('offer_accepted', 'Offer accepted'),
                                        ('sold', 'Sold'),
                                        ('canceled', 'Canceled')],
                             default='new',
                             required=True,
                             string='Status',
                             copy=False)
    active = fields.Boolean(default=True)
    is_available = fields.Boolean(compute='_compute_is_available')
    property_type_id = fields.Many2one(comodel_name='estate.property.type')
    salesman = fields.Many2one(comodel_name='res.users',
                               default=lambda self: self.env.user)
    buyer = fields.Many2one(comodel_name='res.partner', copy=False)
    tag_ids = fields.Many2many(comodel_name='estate.property.tag')
    offer_ids = fields.One2many(comodel_name='estate.property.offer',
                                inverse_name='property_id')
    total_area = fields.Integer(string='Total area (sqm)',
                                compute='_compute_total_area')
    best_price = fields.Float(string='Best offer',
                              compute='_compute_best_offer')

    _sql_constraints = [('check_expected_price', 'CHECK(expected_price > 0)', 'Price must be greater than zero'),
                        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Price must be greater than zero')]

    def _compute_is_available(self):
        for rec in self:
            # if rec.date_availability==False:
            if not rec.date_availability:
                rec.available = False
            else:
                rec.available = (rec.date_availability <= fields.Date.today())

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for rec in self:
            # rec.best_price = 0
            # for offer in rec.offer_ids:
            #     if offer.price > rec.best_price:
            #         rec.best_price = offer.price
            if len(rec.offer_ids) > 0:
                rec.best_price = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _ondelete_estate_property(self):
        for rec in self:
            if rec.state not in ('new', 'canceled'):
                raise ValidationError(_('Only new and canceled properties can be deleted.'))
                # None

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val['garden'] and val['garden_orientation'] is False:
                val['garden_orientation'] = 'north'
            else:
                val['garden_orientation'] = False
        return super().create(vals_list)

    def action_do_sold(self):
        for rec in self:
            if rec.buyer.id is False:
                raise UserError(_('No  accepted offers. To sell you must accept the offer'))
            if rec.state == 'canceled':
                raise UserError(_('Canceled properties cannot be sold'))
            rec.state = 'sold'
            rec.selling_price = rec.best_price

    def action_do_cancel(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(_('Sold property cannot be canceled'))
            rec.state = 'canceled'
            rec.selling_price = 0

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for rec in self:
            # if rec.state == 'sold' and rec.selling_price < rec.expected_price * 0.9:
            if rec.selling_price < rec.expected_price * 0.9 and not float_is_zero(rec.selling_price, precision_digits=2):
                raise ValidationError(_('The selling price must be least 90% of the expected price! '
                                        'You must reduce the expected  price if you want to accept this offer'))

    def set_state_offer_received(self):
        for rec in self:
            rec.state = 'offer_received'

    def is_price_acceptable(self, offer_price):
        if offer_price == 0:
            return False
        for rec in self:
            if len(rec.offer_ids) > 0:
                max_offer = max(rec.offer_ids.mapped('price'))
                if max_offer > offer_price:
                    raise ValidationError(_(f'The offer must be higher then {max_offer}'))
                    # return False
        return True
