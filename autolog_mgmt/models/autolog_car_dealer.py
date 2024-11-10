from odoo import models, fields, api
from odoo.exceptions import ValidationError

from odoo.addons.payment_stripe.utils import format_shipping_address


class AutologisticCarDealer(models.Model):
    _name = 'autolog.car.dealer'
    _inherit = "mail.thread"
    _description = 'Car dealer'

    name = fields.Char(
        string="Dealer",
        required=True,
    )
    contact_person_ids = fields.Many2many(
        comodel_name="res.partner",
    )
    phone = fields.Char(

    )
    email = fields.Char(

    )
    address = fields.Char(

    )

    cars_ids = fields.One2many(
        comodel_name='autolog.receive.car',
        inverse_name='dealer_id',
        string="Received Cars",
    )
    cars_quantity = fields.Integer(
        compute="_compute_cars_quantity"
    )

    @api.onchange('cars_ids')
    def _onchange_cars_ids(self):
        """Trigger a warning if any car has a remark.

                Returns:
                    dict: Warning message if any field is_remark = True.
                """
        for rec in self:
            if rec.cars_ids:
                for car in rec.cars_ids:
                    if car.is_remark:
                        return {
                            'warning': {
                                'title': 'Warning',
                                'message': (
                                    'Don`t forget to write remark description'
                                )
                            }
                        }
        return {}

    @api.onchange('cars_ids')
    def _compute_cars_quantity(self):
        for rec in self:
            rec.cars_quantity = len(rec.cars_ids.filtered(
                lambda car: car.status == 'sent_to_dealer'))
