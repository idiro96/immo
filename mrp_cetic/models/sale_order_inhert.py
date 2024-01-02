# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StockMoveInherited(models.Model):
    _inherit = "stock.move"


    quantity_in_stock = fields.Float(
        string='Quantity in Stock',
        related='product_id.qty_available',
        readonly=True
    )

class PurchaseOrderInherited(models.Model):
    _inherit = "purchase.order"


    production_id = fields.Many2one('mrp.production')


class MrpProdInherited(models.Model):
    _inherit = "mrp.production"

    article_id = fields.Many2one('mrp_cetic.effectuer.achat')

    purchase_order_ids = fields.One2many('purchase.order', 'production_id', string='Purchase Orders')



    purchase_order_count = fields.Integer(
        string='Purchase Orders',
        compute='get_achat_count',

    )


    def get_achat_count(self):
        count = self.env['purchase.order'].search_count([('product_id', '=', self.id)])
        self.purchase_order_count = count


    @api.multi
    def open_produce_product(self):
        result = super(MrpProdInherited, self).open_produce_product()
        insufficient_products = []

        for rec in self.move_raw_ids:
            if rec.product_uom_qty > rec.reserved_availability:
                insufficient_products.append(rec.product_id.display_name)

        if insufficient_products:
            product_names = '\n - '.join(insufficient_products)
            raise ValidationError("Vous ne pouvez pas produire l\'article, la quantité est insufisante pour: \n - %s" % product_names)


        return result


    @api.multi
    def open_purchase_view(self):
        self.ensure_one()
        purchase = self.env[('purchase.order')].search([('product_id', '=', self.id)])

        return {
            'name': 'Purchase',
            'view_mode': 'form' if len(purchase) == 1 else 'tree,form',
            'res_model': 'purchase.order',
            'res_id': purchase.id if len(purchase) == 1 else None,
            'type': 'ir.actions.act_window',
            'domain': [('product_id', '=', self.id)],
        }



    # @api.multi
    # def open_produce_product(self):
    #     result = super(MrpProdInherited, self).open_produce_product()
    #     for rec in self.move_raw_ids:
    #         print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    #         print(rec)
    #         for rec1 in rec.product_id.product_tmpl_id:
    #             print(rec1)
    #             if rec.product_uom_qty > rec.reserved_availability:
    #                 raise ValidationError('vous ne pouvez pas produire l\'article,la quantité est insufisante pour %s' % rec1.name)
    #     return result

    #
    #
    # @api.depends('mouv_raw_ids.product_id')
    # def _compute_quantity_in_stock(self):
    #     stock_quant = self.env['stock.quant']
    #     for production in self:
    #         quantity = 0.0
    #         for raw in production.mouv_raw_ids:
    #             # Here you'll need to adjust the domain to fit your needs
    #             quants = stock_quant.search([('product_id', '=', raw.product_id.id)])
    #             quantity += sum(quants.mapped('quantity'))
    #         production.quantity_in_stock = quantity

    # @api.multi
    # def effectuer_achat(self):
    #     return {
    #         'name': 'Effectuer Achat',
    #         'view_type': 'form',
    #         'res_model': 'purchase.order',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'type': 'ir.actions.act_window',
    #         'target': 'current'
    #     }



