


from odoo import models,fields,api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    category_sequence_id = fields.Many2one('ir.sequence', 'Sequence')

class ProductGroupType(models.Model):
    _name='product.group.type'
    _description = 'Product Group Type'


    name = fields.Char('Name')

class ProductSideType(models.Model):
    _name='product.side.type'
    _description = 'Product Side Type'


    name = fields.Char('Name')

class ProductKumasType(models.Model):
    _name='product.kumas.type'
    _description = 'Product Kumas Type'


    name = fields.Char('Name')




class ProductTemplate(models.Model):
    _inherit='product.template'


    group_type_id = fields.Many2one('product.group.type','Product Group Type')
    gramaj = fields.Float('Gramaj')
    en = fields.Float('En')
    boy = fields.Float('Boy')
    kenar_id = fields.Many2one('product.side.type','Product Side Type')
    kumas_type_id = fields.Many2one('product.kumas.type','Kumas Type')
    kumas_gramaj = fields.Float('Kumaş Gramajı')


    @api.model_create_multi
    def create(self, vals_list):
        res = super(ProductTemplate, self).create(vals_list)
        for product in res:
            if product.categ_id and product.categ_id.category_sequence_id:
                product.default_code = product.categ_id.category_sequence_id.next_by_id()
        return res



class SaleOrder(models.Model):
    _inherit='sale.order'

    delivery_slip_no = fields.Char(compute='_compute_delivery_slip_no')

    def _compute_delivery_slip_no(self):
        for sale in self:
            if sale.order_line:
                sale.delivery_slip_no = sale.mapped('order_line.move_ids.picking_id').filtered(lambda l:l.state=='done').mapped('name')