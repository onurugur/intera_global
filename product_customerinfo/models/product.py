


from odoo import models,fields,api



class ProductTemplate(models.Model):
    _inherit='product.template'
    
    
    
    
    
    customerinfo_ids = fields.One2many('product.customerinfo','product_id','Customer Names')
