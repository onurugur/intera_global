# -*- encoding: utf-8 -*-

{
    'name' : 'Import Bom from Excel',
    'category' : 'Onur',
    'depends' : ['mrp','product'],
    'author': 'Codequarters',
    'license':'LGPL-3',
    'website': 'http://www.onur.com',
    'description': """ Import Bom from Excel """,
    'data': [
        'security/ir.model.access.csv',
        'views/import_bom_views.xml',
    ]
}
