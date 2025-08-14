from datetime import timedelta
from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Info on real estate properties"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        'Available From', copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean('Active', default=True)

    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer_Accepted'),
            ('sold', 'Sold'), ('cancelled', 'Cancelled')
            ],
        required=True, copy=False, default='new'
    )

    # Many-to-One relationship between estate property and estate property type
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")

    # Buyer can be any individual
    buyer_id = fields.Many2one("res.partner", string='Buyer', copy=False)

    # Salesperson has to be an employee (Odoo user)
    user_id = fields.Many2one(
        "res.users", string='Salesperson', default=lambda self: self.env.user)

    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")

    offer_ids = fields.One2many("estate.property.offer", "property_id")
