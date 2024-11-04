from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AutologisticCarBrands(models.Model):
    _name = 'autolog.car.brands'
    _inherit = "mail.thread"
    _description = 'Car brands'
    _rec_name = 'complete_name'

    name = fields.Char(string="Model", index='trigram', required=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name', recursive=True,
        store=True)
    parent_id = fields.Many2one('autolog.car.brands', 'Brand',
                                index=True, ondelete='cascade')
    parent_path = fields.Char(index=True, unaccent=False)
    child_id = fields.One2many('autolog.car.brands', 'parent_id',
                               'Child Categories')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name
