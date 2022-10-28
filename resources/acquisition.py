from datetime import date
from time import strftime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_uploads import UploadNotAllowed
from flask import request, send_file, Response, send_from_directory, stream_with_context, render_template
from flask_restful import Resource
import image_helper

from werkzeug.utils import secure_filename
import os
import io
from base64 import encodebytes
from PIL import Image

from db import db
from models import AcquisitionModel
from schemas import AcquisitionSchema

blp = Blueprint("Acquisitions", "acquisitions", description="Operations on acquisitions")


"""
To encode images into byte64 if one chooses to do so
We use different approaches however
"""
def get_response_image(image_path):
    pil_image = Image.open(image_path, mode='r')
    byte_arr = io.BytesIO()
    pil_image.save(byte_arr, format='PNG') 
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img

@blp.route("/acquisition/<string:acquisition_id>")
class Acquisition(MethodView):
    @blp.response(200, AcquisitionSchema)
    def get(self, acquisition_id):
        acquisition= AcquisitionModel.query.get_or_404(acquisition_id)
        return acquisition


    def delete(self, acquisition_id):
        acquisition = AcquisitionModel.query.get_or_404(acquisition_id)
        print(type(acquisition))
        print(acquisition)
        file_path=acquisition.retina_image
        os.remove("static/images/" + file_path)
        db.session.delete(acquisition)
        db.session.commit()
        return {"message": "Acquisition deleted."}

@blp.route("/acquisition/download/<string:acquisition_id>")
class AcquisitionImageDl(MethodView):
        def get(self, acquisition_id):
            acquisition= AcquisitionModel.query.get_or_404(acquisition_id)
            uploads = os.path.join("static", "images")
            return send_from_directory(directory=uploads, path=acquisition.retina_image)
        
        
            
# Used to return the json with the base64 image encoded in the retina_image field instead of the file path
@blp.route("/acquisition/list1/<string:patient_id>")
class AcquisitionList(MethodView):
    @blp.response(200, AcquisitionSchema(many=True))
    def get(self, patient_id):
        acquisition = AcquisitionModel.query.filter(AcquisitionModel.patient_id==patient_id).all()
        
        for acq in acquisition:
            byte64_retina = get_response_image((image_helper.get_path(acq.retina_image, folder="")))
            acq.retina_image = byte64_retina
            print(type(acq))
        return acquisition
        
"""Another approach is to write the function using the help of yield, 
however due to the nature of flask not being multi-threaded,
the display of images weren't successful at this time"""

@blp.route("/acquisition/list2/<string:patient_id>")
class AcquisitionList2(MethodView):
    @blp.response(200, AcquisitionSchema(many=True))
    def get(self, patient_id):
        acquisition = AcquisitionModel.query.filter(AcquisitionModel.patient_id==patient_id).all()

        def stream_image_json(acquisition):
            for acq in acquisition:
                yield send_file(image_helper.get_path(acq.retina_image, folder=""))
                yield "The acquisition id is: " + str(acq.id)
                yield '\n'
                yield "eye: " + acq.eye
                yield '\n'
                yield "date taken: " + strftime(str(acq.date_taken))
                yield '\n'
                yield "site: " + acq.site_name
                yield '\n'
                yield "operator name: " + acq.operator_name
                yield '\n'
                
        return Response(stream_with_context(stream_image_json(acquisition=acquisition)))


@blp.route("/acquisition/list3/<string:patient_id>")
class AcquisitionList3(MethodView):
    def get(self, patient_id):
        acquisition = AcquisitionModel.query.filter(AcquisitionModel.patient_id==patient_id).all()

        return render_template("acquisitionlist.html", acquisition = acquisition)



@blp.route("/acquisition")
class AcquisiionList(MethodView):
    @blp.response(200, AcquisitionSchema(many=True))
    def get(self, patient_id):
        return AcquisitionModel.query.all(patient_id)

    @blp.arguments(AcquisitionSchema)
    @blp.response(201, AcquisitionSchema)
    def post(self, data):
        retina = request.files['data']
        patient_id=request.form.get('patient_id')
        folder=f"patient_{patient_id}"
        try:
            image_path = image_helper.save_image(retina, folder=folder)
            basename = image_helper.get_basename(image_path)
            print({"message": "Image '{}' uploaded.".format(basename)}, 201)
        except UploadNotAllowed: 
            extension = image_helper.get_extension(data["image"])
            print({"Extension '{}' is not allowed.".format(extension)}, 400)

        acquisition=AcquisitionModel(retina_image=image_path, eye=request.form.get('eye'), date_taken=date.fromisoformat(request.form.get('date_taken')), operator_name=request.form.get('operator_name'), site_name=request.form.get('site_name'), patient_id=patient_id)
    
        try:
            db.session.add(acquisition)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return acquisition
        