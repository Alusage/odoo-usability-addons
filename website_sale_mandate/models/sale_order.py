from datetime import datetime
from odoo import api, fields, models, SUPERUSER_ID, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _show_mandate_action(self):
        for order in self:
            order.show_mandate_action = False
            if order.iban and order.iban != order.partner_id.valid_mandate_id.partner_bank_id.acc_number:
                order.show_mandate_action = True
         

    authorize_iban_direct_debit = fields.Boolean('Active Direct Debit (SEPA)')
    show_mandate_action = fields.Boolean("Show Mandate action", compute='_show_mandate_action')
    iban = fields.Char("IBAN")
    iban_contact = fields.Char('Iban Contact')
    
    @api.multi
    def action_create_partner_mandate(self):
        
        mandate_obj = self.env['account.banking.mandate']
        bank_obj = self.env['res.partner.bank']

        for order in self:
            if order.iban:
                new_bank = bank_obj.create({
                    'acc_number': order.iban,
                    'type': 'iban',
                    'partner_id': order.partner_id.id,
                })

                mandate_obj.create({
                    'format': 'sepa',
                    'type': 'recurrent',
                    'partner_bank_id': new_bank.id,
                    'partner_id': order.partner_id.id,
                    'structure': 'CORE',
                    'recurent_sequence_type': 'first',
                    'signature_date': datetime.today().strftime('%Y-%m-%d'),
                })

        return True