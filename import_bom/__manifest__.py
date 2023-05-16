# -*- encoding: utf-8 -*-

{
    'name' : 'Import Bom from Excel',
    'category' : 'base',
    'depends' : ['mrp','product'],
    'author': 'Onur',
    'license':'LGPL-3',
    'website': '',
    'description': """ Import Bom from Excel """,
    'data': [
        'security/ir.model.access.csv',
        'views/import_bom_views.xml',
    ],
}
