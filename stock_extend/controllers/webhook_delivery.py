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
        authorization = request.httprequest.headers.get("Authorization")
        if not authorization:
            return invalid_response("access_token_not_found", "Missing access_token in request header", 401)
        token = request.env['res.partner'].sudo().search([('authorization', "=", authorization)], limit=1)
        if token.find_one_or_create_token(user_id=token.user_id.id) != authorization:
            return invalid_response("access_token", "Token seems to have expired or invalid", 401)

        request.session.uid = token.user_id.id
        request.uid = token.user_id.id
        return func(self, *args, **kwargs)
    return wrap


class WebhookDeliController(Controller):

    @validate_token
    @route("/api/v1/pickings", type="http", auth="none", methods=["GET"], csrf=False)
    def _get_pickings(self, **payload):
        try:
            response = {"pickings": []}
            pickings = request.env['stock.picking'].search([], limit=10)
            for pck in pickings:
                data = {"picking_id": pck.id,
                        "name": pck.name
                        }
                response["pickings"].append(data)
            return response
        except AccessError as e:
            return invalid_response("Access error", "Error: %s" % e.name)