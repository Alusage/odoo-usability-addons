{
    "name": "Ask SEPA mandate on checkout",
    "version": "14.0.1.0.1",
    "description": "Ask SEPA mandate on website sale checkout",
    "summary": "Ask SEPA mandate on website sale checkout",
    "author": "Nicolas JEUDY",
    "website": "https://github.com/Alusage/odoo-usability-addons",
    "license": "LGPL-3",
    "category": "Generic Modules",
    "depends": [
        "base",
        "website_sale",
        "website_form",
        "account_banking_mandate",
        "account_banking_sepa_direct_debit"
        ],
    "data": [
        "views/sale_order_view.xml",
        "views/templates.xml",
    ],
    "installable": True,
    "application": False,
}
