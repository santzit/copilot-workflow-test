from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    test_field = fields.Boolean(
        string="Test Field",
        help="Boolean test field for tutorial.",
        default=False,
    )
