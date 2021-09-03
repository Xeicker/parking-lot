# Cloud Run API based on Hello World with Cloud Code

This is a REST API that manages a parking lot, has three different actions
    	Add: Which is accessible through http://host:port/carAdd?car=<carid>&tariff=<tariff>. This method creates a car and saves it to a persistent dictionary, and returns a JSON with the format:
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
	List: Which is accessible through http://host:port/list. This method returns a JSON file with the format:
	{
		"message" : "Success",
		"data" :[
			{<car1>},{<car2>}...
		]
	}
	Remove: Which is accessible through http://host:port/carRemove?(location=<parkingSpot>|car=<carid>). This method removes from the persistent dictionary the car with <carid> as its id or the car parked in parking spot number equal to <parkingSpot> and returns a JSON with format:
	{
		"message" : ("Success" | <errorMessage>),
                "Fee" : <fee>,
		"car" : <just removed car with finish parking time added>
	} 
