from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        # Let the template hand a typed Internal Reference to its first variant
        # before we number anything, so references people type are never replaced.
        templates = super(ProductTemplate, self.with_context(gs_skip_product_code=True)).create(vals_list)
        templates = templates.with_env(self.env)
        templates.product_variant_ids._gs_assign_product_code()
        return templates


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        if not self.env.context.get('gs_skip_product_code'):
            products._gs_assign_product_code()
        return products

    def _gs_assign_product_code(self):
        """Fill the Internal Reference of products that have none. Never
        changes a reference that is already set."""
        Sequence = self.env['ir.sequence'].sudo()
        for product in self.sudo().filtered(lambda p: not p.default_code).sorted('id'):
            product.default_code = Sequence.next_by_code('gs.product.code')
