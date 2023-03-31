from odoo import fields, models, api, _
from odoo.exceptions import UserError

class BookingDeliveryBoysWizard(models.TransientModel):
    _name = 'booking.delivery.boys.wizard'
    _description = 'This module fills and confirms info about shipment creating handover to internal carriers.'

    def _get_delivery_order(self):
        return self.env['stock.picking'].sudo().search([('id', '=', self._context.get('default_deli_order_id'))], limit=1)

    def _get_info_receiver(self):
        return self.env['res.partner'].sudo().search([('id', '=', self._get_delivery_order().partner_id.id)], limit=1)

    def _get_cod(self):
        return self._get_delivery_order().sale_id.amount_total if self._get_delivery_order().sale_id.payment_method == 'cod' else 0

    name = fields.Char(string='Name', readonly=True)
    delivery_boy_id = fields.Many2one('res.partner', 'Delivery Boy', required=True)
    delivery_boy_phone = fields.Char(related='delivery_boy_id.phone', string='Phone', required=True, readonly=True)
    receiver_id = fields.Many2one('res.partner', 'Receiver', default=_get_info_receiver, required=True, readonly=True, tracking=True)
    street = fields.Char(related='receiver_id.street', string='Street', readonly=True)
    street2 = fields.Char(related='receiver_id.street2', string='Street 2', readonly=True)
    ward_id = fields.Many2one('res.ward', related='receiver_id.ward_id', string='Ward', readonly=True)
    district_id = fields.Many2one('res.district', related='receiver_id.district_id', string='District', readonly=True)
    city_id = fields.Many2one('res.city', related='receiver_id.city_id', string='City', readonly=True)
    receiver_phone = fields.Char(related='receiver_id.phone', string='Phone', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    delivery_order_id = fields.Many2one('stock.picking', string='Delivery order', default=_get_delivery_order, required=True, readonly=True)
    fee_ship = fields.Monetary(string='Fee ship', currency_field='currency_id')
    cod = fields.Monetary(string='COD', default=_get_cod, currency_field='currency_id')

    @api.onchange('cod')
    def _onchange_cod(self):
        if self.delivery_order_id.sale_id.payment_method == 'cod' and self.delivery_order_id.sale_id.amount_total < self.cod:
            raise UserError(_("COD invalid!"))
        elif self.delivery_order_id.sale_id.payment_method == 'online' and self.cod > 0:
            raise UserError(_('COD invalid!'))

    def action_booking_delivery_boys(self):
        delivery_boys_model = self.env['delivery.boys'].sudo()
        try:
            data = {
                'deli_boy_id': self.delivery_boy_id.id,
                'partner_id': self.receiver_id.id,
                'deli_order_id': self.delivery_order_id.id,
                'fee_ship': self.fee_ship,
                'cod': self.cod,
            }
            self.delivery_order_id.write({
                'is_allotted': True
            })
            print('dataa = ', data)
            delivery_boys_model.create(data)
        except Exception as error:
            raise ValueError(_("Something went wrong when create data!\n Error: %s" % str(error)))
        return True