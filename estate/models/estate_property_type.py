from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(required=True)

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "Type names must be unique.")]
