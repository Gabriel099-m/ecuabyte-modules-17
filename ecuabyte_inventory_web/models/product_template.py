from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_publish_to_shop = fields.Boolean(
        string='Publicar en Tienda',
        default=False,
        help='Si esta marcado, el producto se mostrara en la tienda online.',
    )

    def write(self, vals):
        if 'x_publish_to_shop' in vals:
            vals['is_published'] = vals['x_publish_to_shop']
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'x_publish_to_shop' in vals:
                vals['is_published'] = vals['x_publish_to_shop']
        return super().create(vals_list)
