from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritCertification(models.Model):
    _inherit = "hr.employee"

    skype_name = fields.Char("Skype name")
    joining_date = fields.Date("Joining Date")
    certificate_ids = fields.One2many('employee.certificate', 'employees_id', string="Certificate")


class EmployeesCertification(models.Model):
    _name = 'employee.certificate'
    _description = "Employee Certification"

    certificate_name = fields.Many2one('employee.certificate.name', string="Certificate name", required=True)
    issued_by = fields.Many2one('employee.certificate.issued', string="Issued by", required=True)
    start_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")
    date_diff = fields.Char(string="Duration", readonly=True)
    status = fields.Selection([
        ('complete', 'Complete'),
        ('progress', 'In progress'),
        ('certified', 'Certified')
    ], tracking=True, required=True)
    upload_file = fields.Binary(string="Upload file")
    employees_id = fields.Many2one('hr.employee', string="Certificate")

    @api.constrains('start_date', 'end_date')
    def _check_date_validation(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError('Start date should not greater than end date.')
            else:
                record.date_diff = (record.end_date - record.start_date).days


class CertificationName(models.Model):
    _name = 'employee.certificate.name'
    _description = "Employee Certification name"

    name = fields.Char(string="Certificate name")


class CertificationIssued(models.Model):
    _name = 'employee.certificate.issued'
    _description = "Employee Certification Issued"

    name = fields.Char(string="Certificate Issued by")
