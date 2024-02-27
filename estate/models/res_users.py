from odoo import fields, models


class ResUsers(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _inherit = "res.users"

    # --------------------------------------- Fields Declaration ----------------------------------
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='salesman_id',
                                   domain="[('salesman_id', '=', id)]")
