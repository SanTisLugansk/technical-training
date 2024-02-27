from odoo import models, fields


class EstatePropertyType(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _name = "estate.property.type"
    _description = "Real estate property type"
    _order = "sequence ASC, name ASC"
    _sql_constraints = [("check_name", "UNIQUE(name)", "The name must be unique")]

    # --------------------------------------- Fields Declaration ----------------------------------
    name = fields.Char(required=True)
    sequence = fields.Integer(default=10, help='Use for sorting. Smaller ones first')

    type_line_ids = fields.One2many(comodel_name='estate.property',
                                    inverse_name='property_type_id')

    offer_count = fields.Integer(compute='_compute_offer_count')
    offer_ids = fields.One2many(comodel_name='estate.property.offer',
                                inverse_name='property_type_id')

    # ---------------------------------------- Compute methods ------------------------------------
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
