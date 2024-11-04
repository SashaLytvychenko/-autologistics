from datetime import datetime
from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AutologisticRepairCar(models.Model):
    _name = 'autolog.repair.car'
    _inherit = "mail.thread"
    _description = 'Car repair'
    _rec_name = 'reference'

    reference = fields.Char(
        default="New",
    )
    reference_id = fields.Many2one(
        string="Received car reference",
        comodel_name="autolog.receive.car",
        required=True,
        help="This repair applies to this application for receiving a car.",
    )
    repair_start_date = fields.Date(
        default=fields.Date.today(),
    )
    repair_end_date = fields.Date(

    )
    services_ids = fields.Many2many(
        comodel_name='autolog.repair.car.service',
    )
    repair_notes = fields.Text(
        help="Additional notes or instructions for this repair."
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
        readonly=True,
    )
    services_price = fields.Monetary(
        string="Price",
        store=True,
        compute="_compute_services_price",
        required=True,
        currency_field='company_currency_id',
        default=0.0,
        help="This field calculate full price of all repair services for car"
    )
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")

    @api.depends('services_ids')
    def _compute_services_price(self):
        for rec in self:
            total_service_price = sum(
                service.monetary_price for service in rec.services_ids)
            rec.services_price += total_service_price

    @api.model_create_multi
    def create(self, vals_list):
        priority_days = {
            '0': None,  # Normal - no specific end date
            '1': 2,  # Low - end date +2 days
            '2': 1,  # High - end date +1 day
            '3': 0  # Very High - end date same day
        }

        for vals in vals_list:
            _logger.debug("Processing vals: %s", vals)

            # Проверяем, что vals - это словарь
            if not isinstance(vals, dict):
                _logger.warning("Skipping non-dictionary vals: %s", vals)
                continue

            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'autolog.repair.car')

        start_date = fields.Date.to_date(
            vals.get('repair_start_date') or fields.Date.today())
        days_to_add = priority_days.get(vals.get('priority'))

        if days_to_add is not None:
            vals['repair_end_date'] = start_date + timedelta(days=days_to_add)
        else:
            vals[
                'repair_end_date'] = False  # No end date for 'Normal' priority

        _logger.debug("Final vals_list for creation: %s", vals_list)
        return super().create(vals_list)

    @api.onchange('priority')
    def _deadline(self):
        for rec in self:
            if rec.priority == '1':  # Проверяем на приоритет 'Low'
                if rec.repair_start_date:
                    rec.repair_end_date = rec.repair_start_date + timedelta(
                        days=2)
