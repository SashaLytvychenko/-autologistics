from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AutologisticTruckDriver(models.Model):
    _name = 'autolog.truck.driver'
    _inherit = "mail.thread"
    _description = 'Truck driver'

    name = fields.Char(
        required=True,
    )
    date_birth = fields.Date(

    )
    phone = fields.Char(

    )
    truck_number = fields.Char(
        required=True,
        size=8,
    )
    image = fields.Image(
    )
    driving_experience = fields.Integer(
        string="Driving experience(years):",
        default=2,
    )

    @api.constrains('date_birth')
    def _check_date_birth(self):
        """Check that the birth date is not in the future.

                Raises:
                    ValidationError: If the birth date is greater than
                    today's date.
                    """
        for rec in self:
            if rec.date_birth and rec.date_birth > fields.Date.today():
                raise ValidationError(
                    f'You cannot enter birth date more than today date:'
                    f' {fields.Date.today()}')
