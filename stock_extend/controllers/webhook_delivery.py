import functools
import json
import datetime
import werkzeug.wrappers
from odoo.http import Controller, request, route
from odoo.exceptions import AccessError, UserError, AccessDenied


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, bytes):
        return str(o)


def valid_response(data, message='', status=200):
    """Valid Response
    This will be return when the http request was successfully processed."""
    response = {"status": "success",
                "message": message}
    if len(data) > 0:
        response['data'] = data
    return werkzeug.wrappers.Response(
        status=status, content_type="application/json; charset=utf-8", response=json.dumps(response, default=default),
    )


def invalid_response(typ, message=None, status=401):
    """Invalid Response
    This will be the return value whenever the server runs into an error
    either from the client or the server."""
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(
            {"status": "error", "message": str(message) if str(message) else "wrong arguments (missing validation)"},
            default=datetime.datetime.isoformat,
        ),
    )


def validate_token(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        path = request.httprequest.path
        if 'vtp' in path:
            authorization = request.httprequest.headers.get("Authorization")
            partner_code = 'VTP'
        elif 'ahamove' in path:
            authorization = request.httprequest.headers.get("apikey")
            partner_code = 'AHAMOVE'
        else:
            return invalid_response("path_error", "path is not formatted", 401)
        if not authorization:
            return invalid_response("access_token_not_found", "Missing Authorization in request header", 401)
        token = request.env['res.partner'].sudo().search([('partner_code', '=', partner_code), ('authorization', "=", authorization)], limit=1)
        if token.find_one_or_create_token(partner_id=token.id) != authorization:
            return invalid_response("access_token", "Token seems to have expired or invalid", 401)

        request.session.uid = token.user_id.id
        request.uid = token.user_id.id
        return func(self, *args, **kwargs)
    return wrap

def validate_payload(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        path = request.httprequest.path
        payload = request.jsonrequest

        if 'vtp' in path:
            keys_payload = list(payload['DATA'].keys())
            if 'ORDER_NUMBER' not in keys_payload or 'STATUS_NAME' not in keys_payload:
                order_number = 'ORDER_NUMBER' if 'ORDER_NUMBER' not in keys_payload else False
                status_name = 'STATUS_NAME' if 'STATUS_NAME' not in keys_payload else False
                if order_number or status_name:
                    return invalid_response("payload_invalid", "Payload don't have %s" % "ORDER_NUMBER & STATUS_NAME" if 'ORDER_NUMBER' not in keys_payload and 'STATUS_NAME' not in keys_payload else order_number or status_name, 401)
            else:
                if not payload['DATA']['ORDER_NUMBER']:
                    return invalid_response("data_null", "ORDER_NUMBER is empty!", 401)
                if not payload['DATA']['STATUS_NAME']:
                    return invalid_response("data_null", "STATUS_NAME is empty!", 401)
        elif 'ahamove' in path:
            keys_payload = payload.keys()
            if '_id' or 'status' not in keys_payload:
                order_number = '_id' if '_id' not in keys_payload else False
                status_name = 'status' if 'status' not in keys_payload else False
                return invalid_response("payload_invalid", "Payload don't have %s" % "_id & status" if '_id' not in keys_payload and 'status' not in keys_payload else order_number or status_name, 401)
            else:
                if not payload['_id']:
                    return invalid_response("data_null", "_id is empty!", 401)
                if not payload['status']:
                    return invalid_response("data_null", "status is empty!", 401)
        else:
            return invalid_response("path_error", "path is not formatted", 401)
        return func(self, *args, **kwargs)
    return wrap

class WebhookDeliController(Controller):

    @validate_token
    @validate_payload
    @route('/api/v1/update_delivery_carrier_vtp', type='json', auth='none', methods=["POST"], csrf=False)
    def _update_delivery_carrier_viettel_post(self, **payload):
        try:
            payload = request.jsonrequest
            if not payload:
                return invalid_response("Error", "No data!")
            delivery_book = request.env['delivery.book'].sudo().search([('bl_code', '=', payload['ORDER_NUMBER'])], limit=1)
            if not delivery_book:
                return invalid_response("Error", "Cannot find Delivery Carrier for VTP!")
            delivery_book.write({
                'state': payload['STATUS_NAME'],
            })
            return valid_response(payload, "Successfully!", 200)
        except Exception as error:
            return invalid_response("Update delivery carrier viettel post failed", "Error: %s" % error)

    @validate_token
    @validate_payload
    @route('/api/v1/update_delivery_carrier_ahamove', type='json', auth='none', methods=["POST"], csrf=False)
    def _update_delivery_carrier_ahamove(self, **payload):
        try:
            payload = request.jsonrequest
            if not payload:
                return invalid_response("Error", "No data!")
            delivery_book = request.env['delivery.book'].sudo().search([('bl_code', '=', payload.get('_id'))], limit=1)
            if not delivery_book:
                return invalid_response("Error", "Cannot find Delivery Carrier for Ahamove")
            delivery_book.write({
                'state': payload['status'],
            })
            return valid_response(payload, "Successfully!", 200)
        except Exception as error:
            return invalid_response("Update delivery carrier ahamove failed", "Error: %s" % error)