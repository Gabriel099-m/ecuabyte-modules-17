# -*- coding: utf-8 -*-
{
    'name': 'Ecuabyte Website Custom',
    'version': '17.0.1.1.0',
    'summary': 'Personalizacion del sitio: home, ticket, checkout (ES/EN/PT).',
    'description': """
Ecuabyte Website Custom
=======================
Personalizacion reproducible del sitio web:

* Home (pagina con url "/"): contenido ES / EN / PT.
* Formulario de ticket (website_helpdesk.ticket_submit_form): etiquetas ES / EN / PT.
* Checkout: tipos de identificacion del Ecuador traducidos (ES / EN / PT),
  campo Compania opcional y formulario de direccion en 2 columnas.
    """,
    'author': 'Ecuabyte',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale', 'l10n_ec_website_sale'],
    'data': [
        'data/apply.xml',
        'views/checkout_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ecuabyte_website_custom/static/src/css/ecuabyte_checkout.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
