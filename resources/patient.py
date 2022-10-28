from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import PatientModel
from schemas import PatientSchema


blp = Blueprint("Patients", "patients", description="Operations on patients")


@blp.route("/patient/<string:patient_id>")
class Patient(MethodView):
    @blp.response(200, PatientSchema)
    def get(self, patient_id):
        patient = PatientModel.query.get_or_404(patient_id)
        return patient
    

    def delete(self, patient_id):
        patient = PatientModel.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted"}, 200

@blp.route("/patient/<string:f_name>/<string:l_name>")
class PatientName(MethodView):
    @blp.response(200, PatientSchema(many=True))
    def get(self, f_name, l_name):
        patient = PatientModel.query.filter(PatientModel.first_name==f_name).filter(PatientModel.last_name==l_name).all()
        return patient
    


@blp.route("/patient")
class PatientList(MethodView):
    @blp.response(200, PatientSchema(many=True))
    def get(self):
        return PatientModel.query.all()


    @blp.arguments(PatientSchema)
    @blp.response(201, PatientSchema)
    def post(self, patient_data):
        patient = PatientModel(**patient_data)
        try:
            db.session.add(patient)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A patient with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the patient.")

        return patient