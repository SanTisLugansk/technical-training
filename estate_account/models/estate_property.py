import logging

from odoo import models, fields
from odoo import Command
# from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    account_move_id = fields.Many2one(comodel_name='account.move')

    def action_do_sold(self):
        res = super().action_do_sold()

        _logger.info('estate.account')

        journal = self.env['account.journal'].search(domain=[('type', '=', 'sale'), ('company_id', '=', self.env.company.id)],
                                                     limit=1,
                                                     )

        invoice_values = {'partner_id': self.buyer.id,
                          'move_type': 'out_invoice',
                          'journal_id': journal.id,
                          'invoice_line_ids': [Command.create({'name': self.name,
                                                               'quantity': 1,
                                                               'price_unit': self.selling_price}),
                                               Command.create({'name': '6% of the selling price',
                                                               'quantity': 1,
                                                               'price_unit': self.selling_price*6/100}),
                                               Command.create({'name': 'administrative fees',
                                                               'quantity': 1,
                                                               'price_unit': 100})
                                               ]
                          }
        self.account_move_id = self.env['account.move'].with_context(default_move_type='out_invoice').create(invoice_values)

        return res
