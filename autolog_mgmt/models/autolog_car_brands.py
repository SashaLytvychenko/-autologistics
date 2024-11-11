from odoo import models, fields, api


class AutologisticCarBrands(models.Model):
    """
        Model representing a car brands, by using hierarchical structure
    """
    _name = 'autolog.car.brands'
    _inherit = "mail.thread"
    _description = 'Car brands'
    _rec_name = 'complete_name'

    name = fields.Char(
        string="Model",
        index='trigram',
        required=True,
    )
    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True,
        store=True,
    )
    parent_id = fields.Many2one(
        comodel_name='autolog.car.brands',
        string='Brand',
        index=True,
        ondelete='cascade',
    )
    parent_path = fields.Char(
        index=True,
        unaccent=False,
    )
    child_id = fields.One2many(
        comodel_name='autolog.car.brands',
        inverse_name='parent_id',
        string='Child Categories',
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name
