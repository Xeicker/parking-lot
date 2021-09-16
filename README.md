# Parking lot REST API

This repository contains a REST API that manages a parking lot through three basic operations: list, remove and add a parked car. It is based on Google's Cloud Run API because the hello world example contains everything to run a web API, and if publishing it is required, everything is there to do so in Google Cloud services.


## Installation

To obtain the latest stable code, use the master branch. For the latest working code, use the dev/Main branch. This project needs a few python modules to run, and they are listed in "requirements.txt" since is the file used to make the docker image. At this point the modules needed are:
Flaskv2.0.1+, requestsv2.26.0+, flask-restfulv0.3.9+, webargsv8.0.1+(other version may work but these versions were tested). To run the application, run the app.py.

## DB structure

This project doesn't use an actual database. It uses the shelve module to generate a kind of persistent dictionary. This dictionary only accepts strings as keys, but as values, it accepts almost any python object. For more information about that module, you can visit [shelve module reference](https://docs.python.org/3/library/shelve.html).

There are two kinds of keys used in this project to save information. 
 * Integer-parseable: This represents a location number in the parking lot. The value associated is a string containing a carID
 * Non-integer-parseable: This represents a carID. The value associated is an instance of Car class

## Use of API

This API works through HTTP requests(if running locally, it runs on localhost:8080/). To make them, it is easy to use Postman, a desktop app where you can select the URL, headers, content, and type of request to send it. 

All the next requests need to be sent to to http://<span></span>host:port/cars(i.e. localhost:8080/cars)

### Add Request

Adds a car to the parking lot giving a car id and selecting a tariff. The server assigns a parking spot if available and saves the time when the car entered.

This request is sent to http://<span></span>host:port/cars(i.e. localhost:8080/cars)  using a POST request with a JSON body as follows:
	
	{
		"car":<carID>,
		"tariff":<tariff>
	}
<carID> must be non-parseable to an integer. And <tariff>, by now, needs to be either "hourly" or "daily"

For example: 


	{
		"car": "car1",
 		"tariff": "hourly"
 	}


This method creates a car and saves it to a persistent dictionary, and returns a JSON with the format:
	
	{
		"status" : ("success" | "fail"),
		<if No Error>
		"car" : <carid>,
		"tariff": <tariff>,
		"location": <parkingSpot[0-N]>,
		"start": <startDateTime>,
		<else>
		"message" : <errorMessage>
		<end if>
	}

For example

	{
		"status": "success",
		"car": "car1",
		"tariff": "hourly", "location": 12,
		"start": "2014-10-01 14:11:45"
	}	
	
	or

	{
		"status" : "fail",
		"message" : "Tariff argument missing"
	}

Possible error messages are:
  * "missing car argument"
  * "missing tariff argument"
  * "car argument must be a non integer non empty string"
  * "tariff has to be one of: \<tariff_a> ,\<tariff_b>,\<tariff_c>..."
  * Combination of previous two
  * This car id has already been registered
  * Parking lot is full

### List Request

Lists all cars on the parking lot
			
This request is sent to http://<span></span>host:port/cars(i.e. localhost:8080/cars)   using a GET request. This method returns a JSON file cointaining all cars in the parking lot with the format:
	
	{
		"status" : "success",
		"cars" :[
			{<car1>},{<car2>}...
		]
	}
	
Where cars are represented as:
	
	{
		"car" : <carid>,
		"tariff": <tariff>,
		"location": <parkingSpot[0-N]>,
		"start": <startDateTime>
	}

For example:

  	{
	  "status": "success",
	  "cars" : [
    	{
			"car": "car1",
			"tariff": "hourly",
			"location": 1,
			"start": "2014-10-01 14:11:45"
		},
        {
			"car": "car2",
			"tariff": "daily",
			"location": 2,
			"start": "2014-10-01 15:23:05"
		}
    ] }

###  Remove Request

Removes a car from the parking lot and calculates the fee based on the time elapsed from the addition of the car to removing it, using the selected tariff.

This request is sent to http://<span></span>host:port/cars(i.e. localhost:8080/cars) using a DELETE request with a JSON body as follows:

	{
		"car" : <carID>
		<or>
		"location" : <location>
	}

The <carID> has to be a string non-integer-parseable, this parameter is prioritized if present. The <location> has to be an integer.

Example JSON body: 

	{
		"car" : "car1"
	}

	or

	{
		"location" : 3 
	}

 This method removes from the persistent dictionary the car with that <carID> or <location> property and returns a JSON with the format:
	
	{
		"status" : ("success" | "fail")
		<if error>
		"message" : <errorMessage>,
		<else>
    	"fee" : <fee>,
		"car" : <carid>,
		"tariff": <tariff>,
		"location": <parkingSpot[0-N]>,
		"start": <startDateTime>,
		"finish" : <finishDateTime>
		<end if>
	} 

For example
	
	{
		"status": "success",
	 	"car": "car1", 
		"tariff": "hourly", 
		"location": 12, 
		"start": "2014-10-01 14:11:45"
		"finish": "2014-10-01 14:21:57",
	}

Possible error messages:
  * "missing car argument, request needs to contain either location or car argument"}
  * "car argument must be non-integer"
  * "car not found"
  * "Invalid location" : when the given location is a bigger number than available parking spots
  * "Location was free"