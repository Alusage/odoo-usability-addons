# -*- coding: utf-8 -*-
import json
import logging

from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSaleForm

_logger = logging.getLogger(__name__)


class WebsiteSaleFormCustom(WebsiteSaleForm):
    @http.route(
        "/website_form/shop.sale.order",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def website_form_saleorder(self, **kwargs):
        custom_data = {}
        # TODO: properly inherit with super()
        # response = super(WebsiteSaleFormCustom, self).website_form_saleorder(**post)
        model_record = request.env.ref("sale.model_sale_order")
        # TODO: test iban number
        try:
            data = self.extract_data(model_record, kwargs)
        except ValidationError as e:
            return json.dumps({"error_fields": e.args[0]})

        for keys in data["custom"].split("\n"):
            value, value_data = keys.split(":")
            custom_data[value.strip()] = value_data.strip()

        order = request.website.sale_get_order()
        if data["record"]:
            order.write(data["record"])

        if custom_data:
            if custom_data['iban']:
                custom_data['authorize_iban_direct_debit'] = True
            order.write(custom_data)

        if data["custom"]:
            values = {
                "body": nl2br(data["custom"]),
                "model": "sale.order",
                "message_type": "comment",
                "no_auto_thread": False,
                "res_id": order.id,
            }
            request.env["mail.message"].sudo().create(values)

        if data["attachments"]:
            self.insert_attachment(model_record, order.id, data["attachments"])

        return json.dumps({"id": order.id})
