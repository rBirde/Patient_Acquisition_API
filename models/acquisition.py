
from db import db


class AcquisitionModel(db.Model):
    __tablename__ = "acquisitions"

    id = db.Column(db.Integer, primary_key=True)
    eye = db.Column(db.Enum('left', 'right', name='varchar'), nullable = False)
    site_name = db.Column(db.String(80), unique = False, nullable = False)
    date_taken = db.Column(db.Date, nullable = False)
    operator_name = db.Column(db.String(80), unique = False, nullable = False)
    retina_image = db.Column(db.Text, unique=True, nullable=False)
    patient_id = db.Column(
        db.Integer, db.ForeignKey("patients.id"), unique=False, nullable=False
    )
    patient = db.relationship("PatientModel", back_populates="acquisitions")
