from datetime import datetime
from datetime import timedelta

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
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
        help="This repair applies to this application for receiving a car.",
    )
    repair_start_date = fields.Date(
        default=fields.Date.today(),
    )
    repair_end_date = fields.Date(

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

    product_ids = fields.Many2many(
        comodel_name='product.product',
        string="Services",
        help="Product related to this repair service.",
        domain = [("detailed_type","=","service")],
    )

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")

    repair_duration_days = fields.Integer(
        string="Repair Duration (Days)",
        compute="_compute_repair_duration_days",
        store=True,
        help="Automatically calculated based on repair start and end dates."
    )

    total_price = fields.Monetary(
        store=True,
        compute="_compute_total_price",
        currency_field='company_currency_id',
        readonly  = False
    )
    sale_order_id = fields.Many2one(
        comodel_name = 'sale.order',
        string="Sale Order",
        help="Linked sale order for this repair."
    )

    partner_id = fields.Many2one(
        comodel_name = "res.partner"
    )

    status = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('in_progress', 'In progress'),
                   ('done', 'Done'),],
        default='draft',
        tracking=True,
    )



    @api.depends('product_ids')
    def _compute_total_price(self):
        for repair in self:
            repair.total_price = sum(
                product.list_price for product in repair.product_ids)



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                    vals['reference'] = self.env['ir.sequence'].next_by_code(
                        'autolog.repair.car')

        return super().create(vals_list)

    @api.onchange('priority')
    def _deadline(self):
        for rec in self:
            if rec.priority == '1':  # Проверяем на приоритет 'Low'
                if rec.repair_start_date:
                    rec.repair_end_date = rec.repair_start_date + timedelta(
                        days=2)



    def action_create_sale_order(self):
        # Проверка, что у всех записей указаны нужные данные перед созданием заказов на продажу
        for repair in self:
            if repair.sale_order_id:
                raise UserError(
                    _("You cannot create a sale order for a repair that is already linked. "
                      "Affected repair: %s") % repair.reference
                )
            if not repair.partner_id:
                raise UserError(
                    _("A customer is required to create a sale order. "
                      "Affected repair: %s") % repair.reference
                )

        for repair in self:
            # Получение склада по компании
            warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', repair.company_id.id)], limit=1)
            if not warehouse:
                raise UserError(
                    _("Warehouse is not defined for the company %s.") % repair.company_id.name)

            # Основные значения заказа на продажу
            sale_order_values = {
                "partner_id": repair.partner_id.id,
                "company_id": repair.company_id.id,
                "warehouse_id": warehouse.id,
                "origin": repair.reference,
            }
            sale_order = self.env['sale.order'].create(sale_order_values)
            repair.sale_order_id = sale_order

            # Добавление строки заказа для каждого продукта в product_ids
            if not repair.product_ids:
                raise UserError(_("Repair %s does not have any linked products.") % repair.reference)

            for product in repair.product_ids:
                sale_order_line_values = {
                    "order_id": sale_order.id,
                    "product_id": product.id,
                    "name": product.display_name,
                    "product_uom_qty": 1,  # Укажите нужное количество
                    "price_unit": product.list_price,  # Используем стандартную цену продукта или настраиваемую цену
                }
                self.env['sale.order.line'].create(sale_order_line_values)

        # Показ связанного заказа на продажу
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sale Order'),
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
        }


