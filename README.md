# Cloud Run API based on "Hello World with Cloud Code"

his is a REST API that manages a parking lot, has three different actions
 
# Add
Which is accessible through http://host:port/cars  using a POST request with a JSON body as follows:
	{
		"car":<carID>
		"tariff":<tariff>
	}
<carID> must be non-parseable to an integer. And <tariff>, by now, needs to be either "hourly" or "daily"
This method creates a car and saves it to a persistent dictionary, and returns a JSON with the format:
	{
		"message" : ("Success" | <errorMessage>)
		<if No Error>"data" : <car>
	}
	where a car is represented as:
	{
		"car" : <carid>
		"tariff": <tariff>
		"location": <parkingSpot[0-N]>
		"start": <startDateTime>
	}
Possible error messages are:
	Missing arguments on the request: either carID or tariff parameters are missing
	Invalid arguments on the request: if <carID> length is zero, or is parseable to integer; or if <tariff> is not recognized
        This car id has already been registered: self-explanatory
        Parking lot is full: self-explanatory
# List
Which is accessible through http://host:port/cars using a GET request. This method returns a JSON file cointaining all cars in the parking lot with the format:
	{
		"message" : "Success",
		"data" :[
			{<car1>},{<car2>}...
		]
	}
# Remove

Which is accessible through http://host:port/cars/<identifier> using a DELETE request. The identifier is taken as <location> if it is an integer or as <carID> otherwise. This method removes from the persistent dictionary the car with that represent <identifier> and returns a JSON with the format:
	{
		"message" : ("Success" | <errorMessage>),
                "Fee" : <fee>,
		"car": <just removed car with finish parking time added>
	} 
Possible error messages:
	Car not found: a car with given <carID> hasn't been registered.
	Invalid location: <location> given is greater than parking lot spots number
	Location was free: no car was on <location>