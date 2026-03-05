from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    test_field = fields.Boolean(
        string="Campo de Teste",
        help="Campo booleano de teste tutorial.",
        default=False,
    )
