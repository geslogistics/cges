# -*- coding: utf-8 -*-

{
    'name': 'GES Logistics',
    'summary': """
        GES Logistics
    """,
    'version': '1.6',
    'author': 'GES Logistics',
    'category': 'freight',
    'company': 'GES Logistics',
    'maintainer': 'GES Logistics',
    'website': "https://www.geslogistics.com",
    'depends': ['product',
                'sale',
                ],
    'data': [
        # Views
        'security/ir.model.access.csv',
        'views/product_category_view.xml',
        'views/product_template_view.xml',
        'views/sale_order_view.xml',
        'views/logistics_freight_address_view.xml',
        'views/logistics_freight_port_view.xml',
        'views/logistics_freight_incoterms_view.xml',
        'views/logistics_shipment_order_view.xml',
        'views/logistics_transport_order_view.xml',
        'views/logistics_storage_order_view.xml',
        'views/logistics_customs_order_view.xml',
        'views/logistics_service_order_view.xml',
        'views/menu.xml',
        'data/logistics_sequence_data.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'OPL-1',
}
