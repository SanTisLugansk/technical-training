import logging

from odoo import models, fields, Command
# from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _inherit = 'estate.property'

    # --------------------------------------- Fields Declaration ----------------------------------
    account_move_id = fields.Many2one(comodel_name='account.move')

    # ---------------------------------------- Action Methods -------------------------------------
    def action_do_sold(self):
        res = super().action_do_sold()

        _logger.info('estate.account')

        journal = self.env['account.journal'].search(domain=[('type', '=', 'sale'), ('company_id', '=', self.env.company.id)], limit=1,)
        # Another way to get the journal:
        # journal = self.env["account.move"].with_context(default_move_type="out_invoice")._get_default_journal()

        for rec in self:
            invoice_values = {'partner_id': rec.buyer_id.id,
                              'move_type': 'out_invoice',
                              'journal_id': journal.id,
                              'invoice_line_ids': [Command.create({'name': rec.name,
                                                                   'quantity': 1.0,
                                                                   'price_unit': rec.selling_price * 6.0 / 100.0}),
                                                   Command.create({'name': 'Administrative fees',
                                                                   'quantity': 1.0,
                                                                   'price_unit': 100.0})
                                                   ]
                              }
            rec.account_move_id = self.env['account.move'].create(invoice_values)
        return res
