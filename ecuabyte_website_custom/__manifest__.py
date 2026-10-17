# -*- coding: utf-8 -*-
{
    'name': 'Ecuabyte Website Custom',
    'version': '17.0.1.0.0',
    'summary': 'Re-aplica las traducciones ES/EN/PT del home y del formulario de ticket.',
    'description': """
Ecuabyte Website Custom
=======================
Este modulo re-aplica de forma reproducible las traducciones del sitio:

* Home (pagina con url "/"): contenido ES / EN / PT.
* Formulario de ticket (website_helpdesk.ticket_submit_form): etiquetas ES / EN / PT.

Se ejecuta al instalar y al actualizar el modulo, por lo que los cambios no se
pierden al reconstruir la base de datos.
    """,
    'author': 'Ecuabyte',
    'license': 'LGPL-3',
    'depends': ['website'],
    'data': [
        'data/apply.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
