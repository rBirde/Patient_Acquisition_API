from marshmallow import Schema, fields, validate


class PlainPatientSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    date_of_birth = fields.Date(required=True)
    sex = fields.Str(validate=validate.OneOf(
        choices=['male', 'female', 'non_binary', 'other'],
        labels=['Male', 'Female', 'Non-binary/fluid', 'Other']
    ))



class PlainAcquisitionSchema(Schema):
    id = fields.Int(dump_only=True)
    eye = fields.Str(validate=validate.OneOf(choices=['left', 'right'], labels=['Left', 'Right']))
    site_name = fields.Str()
    date_taken = fields.Date()
    operator_name = fields.Str()
    retina_image = fields.Str()



class AcquisitionSchema(PlainAcquisitionSchema):
    patient_id = fields.Int(load_only=True)
    patient = fields.Nested(PlainPatientSchema(), dump_only=True)



class PatientSchema(PlainPatientSchema):
    acquisitions = fields.List(fields.Nested(PlainAcquisitionSchema()), dump_only=True)












