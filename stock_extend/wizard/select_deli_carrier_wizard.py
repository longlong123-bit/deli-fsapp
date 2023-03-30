from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SelectDeliveryCarrierWizard(models.TransientModel):
    _name = 'select.delivery.carrier.wizard'
    _description = 'This module is used open a popup to select delivery carrier'

    @api.model
    def default_get(self, fields_list):
        values = super(SelectDeliveryCarrierWizard, self).default_get(fields_list)
        if not values.get('deli_order_id') and 'active_model' in self._context and\
                self._context['active_model'] == 'stock.picking':
            values['deli_order_id'] = self._context.get('active_id')
        return values

    deli_order_id = fields.Many2one('stock.picking', required=True, readonly=True)
    deli_carrier_id = fields.Many2one('delivery.carrier', required=True)

    def action_fill_shipment_info(self):
        if self.deli_carrier_id.delivery_type == 'delivery_boys':
            return {
                'name': _('Delivery Boys Shipment Information'),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': self.env.ref('stock_extend.booking_delivery_boys_wizard_form_view').id,
                'res_model': 'booking.delivery.boys.wizard',
                'context': {'default_deli_order_id': self.deli_order_id.id},
                'type': 'ir.actions.act_window',
                'target': 'new'
            }
        elif self.deli_carrier_id.delivery_type == 'viettelpost':
            return {
                'name': _('Viettelpost Shipment Information'),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': self.env.ref('stock_extend.booking_viettelpost_wizard_form_view').id,
                'res_model': 'booking.viettelpost.wizard',
                'context': {
                    'default_deli_order_id': self.deli_order_id.id,
                    'default_deli_carrier_id': self.deli_carrier_id.id,
                    'default_receiver_id': self.deli_order_id.partner_id.id
                },
                'type': 'ir.actions.act_window',
                'target': 'new'
            }
        elif self.deli_carrier_id.delivery_type == 'ahamove':
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('tr_connect_ahamove.popup_booking_ahamove_wizard_form').id,
                'res_model': 'popup.booking.ahamove',
                'target': 'new'
            }
        else:
            raise ValidationError(_(f'Delivery carrier {self.deli_carrier_id.delivery_type} not found.'))