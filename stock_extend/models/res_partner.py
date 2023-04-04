import hashlib
import os

from odoo import fields, models, api

def nonce(length=40, prefix=""):
    rbytes = os.urandom(length)
    return "{}_{}".format(prefix, str(hashlib.sha1(rbytes).hexdigest()))


class ResPartner(models.Model):
    _inherit = 'res.partner'

    authorization = fields.Char(string='Authorization', help='Authorization of delivery carrier', tracking=True)
    partner_code = fields.Char(string='Code', tracking=True)
    type = fields.Selection(selection_add=[("delivery_carrier", "Delivery Carrier")])

    def get_access_token(self):
        if not self.authorization:
            self.authorization = nonce()

    def find_one_or_create_token(self, partner_id=None, create=False):
        res_partner = self.env['res.partner'].sudo().search([('id', '=', partner_id)], order='id DESC', limit=1)
        if not res_partner:
            return None
        return res_partner.authorization