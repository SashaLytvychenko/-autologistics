from odoo import models, fields, api, _

class AutologisticCarWizard(models.TransientModel):
    _name = 'autolog.car.wizard'
    _description = 'Wizard for Updating Car Status'

    car_id = fields.Many2one(
        'autolog.receive.car',
        string="Car",
        required=True,
        readonly=True
    )
    new_status = fields.Selection(
        selection=[('in_stock', 'In Stock'),
                   ('awaiting_decision', 'Awaiting Decision'),
                   ('repair', 'Repair'),
                   ('sent_to_dealer', 'Sent to Dealer'),
                   ('cancel', 'Cancelled')],
        string="New Status",
        required=True
    )

    def apply_changes(self):
        """Apply the selected status change to the car record."""
        self.ensure_one()
        self.car_id.write({
            'status': self.new_status,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Car Record',
            'view_mode': 'form',
            'res_model': 'autolog.receive.car',
            'res_id': self.car_id.id,
            'target': 'current',
        }
