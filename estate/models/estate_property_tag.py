from odoo import models, fields


class EstatePropertyTag(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _name = "estate.property.tag"
    _description = "Real estate property tag"
    _order = "name"
    _sql_constraints = [('name_unique', 'UNIQUE(name)', "Tag names must be unique.")]

    # --------------------------------------- Fields Declaration ----------------------------------
    name = fields.Char(required=True)
    color = fields.Integer()
