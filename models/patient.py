from tkinter import CASCADE
from db import db


class PatientModel(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    date_of_birth = db.Column(db.Date, nullable = False)
    sex = db.Column(db.Enum('male', 'female', 'non_binary', 'other', name='varchar'), nullable = False)
    acquisitions = db.relationship("AcquisitionModel", back_populates="patient", lazy="dynamic", cascade = "all, delete")