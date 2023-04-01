from odoo import fields, models, api, _


class CancelDeliveryWizard(models.TransientModel):
    _name = 'cancel.delivery.wizard'
    _description = 'Description'

    name = fields.Char()
