# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class AlquilerProducto(models.Model):
    _name = 'alquiler.producto'  #Nombre técnico del modelo
    _description = 'Gestión de Alquiler de Productos'  
    _inherit = ['mail.thread']  

    #Campos básicos
    name = fields.Char(
        string='Referencia', 
        required=True,
        readonly=True,
        default='Nuevo',
        copy=False
    )

    cliente_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        tracking=True
    )

    producto_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True,
        tracking=True
    )

    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        required=True,
        default=fields.Date.today(),
        tracking=True
    )

    fecha_fin = fields.Date(
        string='Fecha de Fin',
        compute='_compute_fecha_fin',
        store=True,
        tracking=True
    )

    state = fields.Selection([
        ('alquiler', 'En Alquiler'),
        ('entregado', 'Entregado'),
        ('no_entregado', 'No Entregado')
    ], string='Estado', default='alquiler', tracking=True)

    observaciones = fields.Text(
        string='Observaciones',
        tracking=True
    )

    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('alquiler.producto') or 'Nuevo'
        return super(AlquilerProducto, self).create(vals)

    #Cálculo automático de la fecha de fin
    @api.depends('fecha_inicio')
    def _compute_fecha_fin(self):
        for record in self:
            if record.fecha_inicio:
                record.fecha_fin = record.fecha_inicio + timedelta(days=30)

    #Verificar disponibilidad del producto
    @api.onchange('producto_id')
    def _onchange_producto(self):
        if self.producto_id:
            #Contar cuántos alquileres activos tiene este producto
            alquileres_activos = self.env['alquiler.producto'].search_count([
                ('producto_id', '=', self.producto_id.id),
                ('state', '=', 'alquiler')
            ])
            if alquileres_activos > 0:
                return {
                    'warning': {
                        'title': 'Advertencia',
                        'message': 'Este producto ya está en alquiler.'
                    }
                }