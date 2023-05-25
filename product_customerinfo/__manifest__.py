{
    'name': 'Product CustomerInfo',
    'version': '11.0.1.0',
    'summary': 'Add product to customerinfo partners',
    'description': """
    Add product a Customerinfo Relation.
    """,
    'author': 'Onur UGUR',
    'company': 'www.andar.com.tr',
    'website': "https://andar.com.tr",
    'depends': ['stock','product'],
    'license':'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
       
    ],
    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False
}


