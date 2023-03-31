from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_allotted = fields.Boolean(default=False)
