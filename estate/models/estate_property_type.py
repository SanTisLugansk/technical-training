from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence ASC, name ASC"

    name = fields.Char(required=True)
    type_line_ids = fields.One2many(comodel_name='estate.property',
                                    inverse_name='property_type_id')
    sequence = fields.Integer(string='Sequence', default=10, help='Use for sorting. Smaller ones first')
