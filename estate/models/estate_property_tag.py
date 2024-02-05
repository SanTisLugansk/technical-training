from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"

    name = fields.Char(required=True)

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "Tag names must be unique.")]
