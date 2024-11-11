from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AutologisticCar(models.Model):
    """
     Model representing the intake and tracking of cars in inventory, including
     attributes, statuses, and locations. It enforces a unique VIN constraint,
     restricts deletion unless in draft status, and includes actions for
     updating statuses and creating repair records.
    """
    _name = 'autolog.receive.car'
    _inherit = "mail.thread"
    _description = 'Receive car'
    _rec_name = 'reference'

    reference = fields.Char(
        default="New",
    )
    vin_code = fields.Char(
        string="VIN",
        required=True,
        size=17
    )
    dealer_id = fields.Many2one(
        comodel_name="autolog.car.dealer",
        string="Dealer name",
    )
    truck_driver_id = fields.Many2one(
        comodel_name="autolog.truck.driver",
    )
    truck_number_id = fields.Char(
        related="truck_driver_id.truck_number",
        readonly=True,
    )

    image = fields.Image(
    )
    car_brand_id = fields.Many2one(
        comodel_name="autolog.car.brands",

    )

    expected_arrival_date = fields.Date(
        help="Expected arrival date when car will be in autologistic stock",

    )
    arrival_date = fields.Date(
        help="The actual date of the car's arrival in stock"

    )
    importer_stock_id = fields.Many2one(
        comodel_name="stock.location",
        domain=[('usage', '=', 'supplier')],
        help="This is the importer's warehouse from which we receive cars "
             "to our warehouse",
    )

    our_stock_id = fields.Many2one(
        comodel_name="stock.location",
        domain=[('usage', '=', 'internal')],
        help="This is our internal stock from which we ship car to the dealer",
    )

    dealer_stock_id = fields.Many2one(
        comodel_name="stock.location",
        domain=[('usage', '=', 'customer')],
        help="This is dealer stock who receives cars from our warehouse"

    )

    status = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('in_stock', 'In stock'),
                   ('awaiting_decision', 'Awaiting decision'),
                   ('repair', 'Repair'),
                   ('sent_to_dealer', 'Sent to dealer'),
                   ('cancel', 'Cancelled')],
        default='draft',
        tracking=True,
    )
    body_type = fields.Selection(
        selection=[('sedan', 'Sedan'),
                   ('hatchback', 'Hatchback'),
                   ('pickup', 'Pickup'),
                   ('crossover', 'Crossover'), ],
        default='sedan',
        tracking=True,
    )
    engine_type = fields.Selection(
        selection=[('petrol', 'Petrol'),
                   ('diesel', 'Diesel'),
                   ('electric', 'Electric'),
                   ('hybrid', 'Hybrid'), ],
        default='petrol',
        tracking=True,
    )

    engine_capacity = fields.Selection(
        selection=[('2.0', '2.0'),
                   ('2.5', '2.5'),
                   ('3.0', '3.0'),
                   ('3.5', '3.5'), ],
        default=None,
        tracking=True,
    )

    transmission = fields.Selection(
        selection=[('manual', 'Manual'),
                   ('automatic', 'Automatic'), ],
        default='automatic',
        tracking=True
    )
    is_seat_heating = fields.Boolean(
        default=False,
    )
    is_wheel_heating = fields.Boolean(
        string="Steering Wheel Heating",
        default=False,
    )
    cruise_control = fields.Selection(
        selection=[('standard', 'Standard'),
                   ('adaptive', 'Adaptive'),
                   ('not available', 'Not available'), ],
        default='standard',
        tracking=True
    )
    is_rearview_camera = fields.Boolean(
        default=False,
    )
    parking_sensors = fields.Selection(
        selection=[('front', 'Front'),
                   ('rear', 'Rear'),
                   ('both', 'Both'),
                   ('none', 'None'),
                   ],
        default='front',
        tracking=True
    )
    mileage = fields.Float(
        default=0.0
    )
    manufacture_date = fields.Date(
        required=True,
    )
    is_service_book = fields.Boolean(
        string="Service book availability",
        default=True,
    )
    is_remark = fields.Boolean(
        default=False,
    )
    remark_description = fields.Text(

    )

    image_remark = fields.Image(

    )

    _sql_constraints = [
        ('vin_uniq', 'unique (vin_code)', 'The VIN code must be unique!')
    ]

    def unlink(self):
        """Unlink method to prevent deletion of receive request with all
        statuses except 'draft' """

        for rec in self:
            if rec.status != 'draft':
                raise ValidationError(_(f'You cannot delete receive request'
                                        f' with this status - {rec.status}'))
        res = super().unlink()
        return res

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'autolog.receive.car')

            # checking that the car's release date cannot be older than today
            if vals.get('manufacture_date'):
                if fields.Date.from_string(
                        vals['manufacture_date']) > fields.Date.today():
                    raise ValidationError(
                        _("Manufacture date cannot be in the future."))
        return super().create(vals_list)

    def write(self, vals):
        """Adding message ot chatter when status = sent_to_dealer """

        if 'status' in vals and vals['status'] == 'sent_to_dealer':
            for rec in self:
                rec.message_post(
                    body=_("The car has been marked as 'Sent to Dealer'."))
        return super().write(vals)

    def action_create_and_open_repair_record(self):
        repair_record = self.env['autolog.repair.car'].create({
            'reference_id': self.id,

        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Car Repair',
            'view_mode': 'form',
            'res_model': 'autolog.repair.car',
            'res_id': repair_record.id,
            'target': 'current',
        }

    @api.onchange('status')
    def _in_stock_status(self):
        """
        """
        for rec in self:
            if rec.status == 'in_stock':
                rec.arrival_date = fields.Date.today()

    def action_in_stock(self):
        for rec in self:
            rec.status = 'in_stock'

    def action_awaiting_decision(self):
        for rec in self:
            rec.status = 'awaiting_decision'

    def action_repair(self):
        for rec in self:
            rec.status = 'repair'

    def action_sent_to_dealer(self):
        for rec in self:
            rec.status = 'sent_to_dealer'

    def action_cancel(self):
        for rec in self:
            rec.status = 'cancel'

    def action_open_status_wizard(self):
        """Open the wizard to update the car status."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Update Car Status'),
            'view_mode': 'form',
            'res_model': 'autolog.car.wizard',
            'target': 'new',
            'context': {
                'default_car_id': self.id,
            },
        }
