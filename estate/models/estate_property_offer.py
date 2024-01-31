import datetime
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'),
                                         ('refused', 'Refused')],
                              copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner',
                                 string='Partner', reguired=True)
    property_id = fields.Many2one(comodel_name='estate.property',
                                  string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline',
                                compute='_compute_date_deadline',
                                inverse='_inverse_deadline_compute_validity')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for rec in self:
            if not rec.create_date:
                create_date = fields.Datetime.now()
            else:
                create_date = rec.create_date
            rec.date_deadline = create_date + datetime.timedelta(days=rec.validity) - datetime.timedelta(days=1)

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
