from odoo import api, fields, models, SUPERUSER_ID, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    authorize_iban_direct_debit = fields.Boolean('Active Direct Debit (SEPA)')
    iban = fields.Char("IBAN")
    iban_contact = fields.Char('Iban Contact')
    