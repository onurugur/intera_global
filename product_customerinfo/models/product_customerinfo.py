



from odoo import models,fields,api




class ProductCustomerinfo(models.Model):
    _name='product.customerinfo'
    _description = "Customer Info"
    
    
    
    sequence = fields.Integer('Sequence',default=1)
    product_id = fields.Many2one('product.template','Product')
    partner_id = fields.Many2one('res.partner','Partner')
    name = fields.Char('Partner Product Name')
    description =fields.Char('Partner Description')
    