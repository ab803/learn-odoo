from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AppOneRealStateProperty(models.Model):
    _name = 'app_one.realstateproperty'
    _description = 'App One Real Estate Property'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today)
    available = fields.Boolean(default=True)
    expected_price = fields.Float(digits=(16, 2))
    selling_price = fields.Float()
    state = fields.Selection([
        ('new', 'New'),
        ('sold', 'Sold'),
    ], default='new')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name of the property must be unique.'),
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms(self):
        for record in self:
            if record.bedrooms < 0:
                raise ValidationError("The number of bedrooms cannot be negative.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'expected_price' in vals and vals['expected_price'] <= 0:
                raise ValidationError("The expected price must be greater than zero.")
        return super().create(vals_list)

    def write(self, vals):
        if 'expected_price' in vals and vals['expected_price'] <= 0:
            raise ValidationError("The expected price must be greater than zero.")
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.state == 'sold':
                raise ValidationError("You cannot delete a property that is sold.")
        return super().unlink()