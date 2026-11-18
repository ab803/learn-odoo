from odoo import models, fields


class AppOneOwner(models.Model):
    _name = 'app_one.owner'
    _description = 'App One Owner'

    name = fields.Char(required=True)
    phone = fields.Char()
    address = fields.Text()