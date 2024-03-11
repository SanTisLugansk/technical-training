import datetime
# from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
# from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _name = 'estate.property.offer'
    _description = 'Real estate property offer'
    _order = 'price desc'
    _sql_constraints = [('check_price', 'CHECK(price > 0)', 'Price must be greater than zero')]

    # --------------------------------------- Fields Declaration ----------------------------------
    price = fields.Float(required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    state = fields.Selection(selection=[('accepted', 'Accepted'),
                                        ('refused', 'Refused')],
                             string="Status", copy=False, default=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', related='property_id.property_type_id', store=True)
    date_deadline = fields.Date(string='Deadline',
                                compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline_validity')

    # ---------------------------------------- Compute methods ------------------------------------
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            # if not rec.create_date:
            #     create_date = fields.Datetime.now()
            # else:
            #     create_date = rec.create_date
            create_date = rec.create_date.date() if rec.create_date else fields.Datetime.today()
            rec.date_deadline = create_date + datetime.timedelta(days=rec.validity) - datetime.timedelta(days=1)

    def _inverse_date_deadline_validity(self):
        for rec in self:
            # if not rec.create_date:
            #     create_date = fields.Datetime.now()
            # else:
            #     create_date = rec.create_date.date()
            create_date = rec.create_date.date() if rec.create_date else fields.Datetime.today()

            # if not rec.date_deadline:
            #     date_deadline = fields.Datetime.now() + datetime.timedelta(days=7)
            # else:
            #     date_deadline = rec.date_deadline
            date_deadline = rec.date_deadline if rec.date_deadline else fields.Datetime.today() + datetime.timedelta(days=7)

            rec.validity = (date_deadline - create_date).days + 1

    # ------------------------------------------ CRUD Methods -------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            offer_price = val['price']
            p = self.env['estate.property'].browse(val['property_id'])
            if not p.is_price_acceptable(offer_price):
                raise ValidationError(_(f'The proposed price of {offer_price} is too low.'))
            p.set_state_offer_received()
        return super().create(vals_list)

    # ---------------------------------------- Action Methods -------------------------------------
    def action_confirm_offer(self):
        # for rec in self:
        #     if rec.state == 'accepted':
        #         return
        #     if self.search_count([('property_id.id', '=', rec.property_id.id),
        #                           ('state', '=', 'accepted')]) > 0:
        #         raise UserError(_('There is already an accepted offer, only one can be accepted'))
        #     rec.state = 'accepted'
        #     # rec.property_id.selling_price = rec.price
        #     rec.property_id.buyer_id = rec.partner_id
        #     rec.property_id.state = 'offer_accepted'

        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError(_("An offer as already been accepted."))
        self.write({"state": "accepted"})
        return self.mapped("property_id").write({"state": "offer_accepted",
                                                 # "selling_price": self.price,
                                                 "buyer_id": self.partner_id.id,
                                                 }
                                                )

    def action_cancel_offer(self):
        # for rec in self:
        #     if rec.state == 'accepted':
        #         # rec.property_id.selling_price = 0
        #         rec.property_id.buyer_id = False
        #     rec.state = 'refused'
        #     rec.property_id.state = 'offer_received'

        self.write({"state": "refused"})
        return self.mapped("property_id").write({"state": "offer_received",
                                                 # "selling_price": 0,
                                                 "buyer_id": False,
                                                 }
                                                )

    def action_delete_offer(self):
        for rec in self:
            rec.unlink()
