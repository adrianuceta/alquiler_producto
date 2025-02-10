{
    'name': 'Alquiler de Productos',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Gestión de alquiler de productos',
    'description': """
        Módulo para gestionar el alquiler de productos a clientes.
        - Registro de préstamos
        - Control de fechas
        - Gestión de estados
    """,
    'author': 'Adrián Uceta Gamaza',
    'depends': [
        'base',
        'sale',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/alquiler_views.xml',
        'data/cron_jobs.xml',
    ],
    'installable': True,
    'application': True,
}