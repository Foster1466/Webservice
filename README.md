# Webservice

## Summary
* Successfully built a webservice for a coding challenge.


## Tech Stack
* Python
* Django


## API Endpoints
###  `POST`
1. Path: `/receipts/process`
   * Method: `POST`
   * Payload: Receipt JSON
   * Response: JSON containing an id for the receipt
   * Example Response:
     `{"id": "70"}`

###  `GET`
2. Path: `/receipts/{id}/points`
   * Method: `GET`
   * Response: JSON containing number of points awarded
   * Example Response:
     `{"points": "65"}`


# Software requirement
To test this project you will need postman
Download using this link: https://www.postman.com/downloads/

Once you finish downloading open postman set up 2 APIs
1. `http://127.0.0.1:8000/receipts/process`
2. `http://127.0.0.1:8000/receipts/<id>/points`

In POST request you will send the payload using Body tab in there select raw and JSON and paste inputs

![image](https://github.com/Foster1466/Webservice/assets/67507979/733e2a3b-82e3-49a0-b8ca-5a37581a9af4)


# Download and setup instructions:
1. Clone project: git clone https://github.com/Foster1466/Webservice.git
2. Open terminal/command prompt and run the following commands:
    1. cd webservice
    2. docker build --tag python-django .
    3. docker run --publish 8000:8000 python-django

    
* In order to test the test scripts, go to the root directory of project and execute the following command:
  
`python manage.py test receipt_processor`
