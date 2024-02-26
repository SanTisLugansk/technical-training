import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'),
                                         ('refused', 'Refused')],
                              copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline',
                                compute='_compute_date_deadline',
                                inverse='_inverse_deadline_compute_validity')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [('check_price', 'CHECK(price > 0)', 'Price must be greater than zero')]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for rec in self:
            if not rec.create_date:
                create_date = fields.Datetime.now()
            else:
                create_date = rec.create_date
            rec.date_deadline = create_date + datetime.timedelta(days=rec.validity) - datetime.timedelta(days=1)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            offer_price = val['price']
            if not self.env['estate.property'].browse(val['property_id']).is_price_acceptable(offer_price):
                raise ValidationError(_(f'The proposed price of {offer_price} is too low.'))
            self.env['estate.property'].browse(val['property_id']).set_state_offer_received()
        return super().create(vals_list)

    def action_confirm_offer(self):
        for rec in self:
            if rec.status == 'accepted':
                return
            if self.search_count([('property_id.id', '=', rec.property_id.id),
                                  ('status', '=', 'accepted')]) > 0:
                raise UserError(_('There is already an accepted offer, only one can be accepted'))
            rec.status = 'accepted'
            # rec.property_id.selling_price = rec.price
            rec.property_id.buyer = rec.partner_id
            rec.property_id.state = 'offer_accepted'

    def action_cancel_offer(self):
        for rec in self:
            if rec.status == 'accepted':
                # rec.property_id.selling_price = 0
                rec.property_id.buyer = False
            rec.status = 'refused'
            rec.property_id.state = 'offer_received'

    def action_delete_offer(self):
        for rec in self:
            rec.unlink()

    def _inverse_deadline_compute_validity(self):
        for rec in self:
            if not rec.create_date:
                create_date = fields.Datetime.now()
            else:
                create_date = rec.create_date.date()
            if not rec.date_deadline:
                date_deadline = fields.Datetime.now() + datetime.timedelta(days=7)
            else:
                date_deadline = rec.date_deadline
            date_interval = date_deadline - create_date
            rec.validity = date_interval.days + 1
