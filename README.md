# POC Patient Acquisition REST API
The available API in this repository provides a RESTful service with CRUD operations for patients and acquisitions. The design is made to work with a large number of images and database. 
The URL mentioned in all the services provided in this API is as follows:

## Patients API
To create a patient the following fields should be specified:
- Patient ID
- First name
- Last name
- Date of birth
- Sex
The patients also store the acquisition information, but while creating a patient it is not required to specify the acquisitions as they could be added later using the patient ID. 
To create a patient use the following url:

while posting a json with the fields mentioned above, note that the date of birth format is _______ and for sex the choices are 'male', 'female', 'non_binary', and 'other' which could be passed as string. Also, patient ID is set to primary key and is not to be mentioned as it will automatically be assigned when the patient is created. 
To get a patient by ID, and First+Last names simply use the following formats, respectively:


To delete a patient simply use the following format and the patient will be deleted from the database. 

## Acquisitions API
To add a new acquisition for a patient, use the following format:

Acquisitions have the following fields:
- Acquisition ID (automatically created)
o Eye (left or right)
o Site name
o Date taken
o Operator name
o Image data - This is the image file being uploaded