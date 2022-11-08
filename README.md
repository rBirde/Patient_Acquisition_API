# POC Patient Acquisition REST API
The available API in this repository provides a RESTful service with CRUD operations for patients and acquisitions. The design is made to work with a large number of images and database. 
Using either Insomnia or Postman is recommended. Using Docker, aws ECR, ECS, and EC2 the API is deployed. The URL mentioned in all the services provided in this API is as follows:
```
http://ec2-18-217-184-148.us-east-2.compute.amazonaws.com
```
## Patients API
To create a patient the following fields should be specified:
- first_name
- last_name
- date_of_birth (YYYY-MM-DD)
- sex ('male', 'female', 'non_binary', and 'other')

while posting a json with the fields mentioned above, note that an ID will be automatically assigned to the patient as it is set to primary key. The patients also store the acquisition information, but while creating a patient it is not required to specify the acquisitions as they could be added later using the patient ID. 

To create a patient use the POST handle with the following address:
```
url/patient
```
To get a patient by ID, and First+Last names simply use the following formats with the GET handle, respectively:
```
url/patient/<string:patient id>
url/patient/<string:first name>/<string:last name>
```
To get a list of all patients simply use the GET handle with the following address:
```
url/patient
```
To delete a patient simply use the following format with the DEL handle and the patient (with associated acquisitions) will be deleted from the database. 
```
url/patient/<string:patient id>
```
## Acquisitions API
To add a new acquisition for a patient, use the GET handle with the following format:
```
url/acquisition
```
Acquisitions have the following fields:
- acquisition_id (automatically created)
- patient_id (the patient for which the acquisitions are made)
- eye (left or right)
- site_name 
- date_taken (YYYY-MM-DD)
- operator_name
- data (which is the retina image being uploaded)
You may use multipart/form-data to upload the acquisitions Images and Information. Use the keys suggested for each field as brought above.
To list all the acquisitions of a patient on file (to show the information of the acquisitions beside their associated images) use the GET handle with the following format:
```
url/acquisition/list3/<string:patient_id>
```
To delete an acquisition use the DEL handle with the following format:
```
url/acquisition/<string:acquisition_id>
```
To Download an image use the GET handle with the following format:
```
url/acquisition/download/<string:acquisition_id>
```
