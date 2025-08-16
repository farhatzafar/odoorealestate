from odoo import fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float(string='Price')
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
        string='Status'
    )

    partner_id = fields.Many2one(
        "res.partner", string='Partner', required=True)

    property_id = fields.Many2one("estate.property", required=True)

    # Compute deadline as sum of offer fields: create_date and validity
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = relativedelta(days=record.validity) + date

    # Inverse function that can set validity from create_date
    def _inverse_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date).days

    validity = fields.Integer(string="Validity (days)", default=7)

    date_deadline = fields.Date(
        string="Deadline", compute=_compute_date_deadline, inverse=_inverse_date_deadline)

    def accept_offer_button(self):
        self.ensure_one()
        if 'accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("This property has already been accepted."))
        else:
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id

    def refuse_offer_button(self):
        self.status = 'refused'
