from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AutologisticRepairCarService(models.Model):
    _name = 'autolog.repair.car.service'
    _inherit = "mail.thread"
    _description = 'Repair Car Service'
    _order = 'sequence,id'

    name = fields.Char(
        string="Service",
        required=True,
    )
    sequence = fields.Integer(
        default=10,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True,
        default=lambda self: self.env.company,
    )
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
    )
    monetary_price = fields.Monetary(
        string='Price',
        required=True,
        currency_field='company_currency_id',
    )
    service_description = fields.Text(

    )
