from datetime import timedelta
from odoo import fields, models, _
from odoo.exceptions import UserError


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
            ('new', 'New'), ('offer_received',
                             'Offer Received'), ('offer_accepted', 'Offer_Accepted'),
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

    # Function to calculate total area baased on: total area = living area + garden area
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    total_area = fields.Integer(string="Total Area (sqm)", compute=(
        _compute_total_area), readonly=True)

    # Function to calculate best price i.e hightest/maximum of the offers' price
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    best_price = fields.Float(
        string="Best Offer", compute=(_compute_best_price))

    def cancel_button(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_("Sold properties cannot be cancelled"))
            else:
                record.state = 'cancelled'

    def sold_button(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_("Cancelled properties cannot be sold"))
            else:
                record.state = 'sold'
