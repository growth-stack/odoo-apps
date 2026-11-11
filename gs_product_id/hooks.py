def post_init_hook(env):
    """Give existing products without an Internal Reference their IDs, oldest first."""
    products = env['product.product'].with_context(active_test=False).search(
        [('default_code', 'in', (False, ''))], order='id')
    products._gs_assign_product_code()
