import requests

# Set your access token obtained from the previous step
access_token = 'BLMUuXruR4tIXGywdos16AESDrG7'

# Define API endpoint and headers
url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Define the query parameters for flight search
params = {
    'originLocationCode': 'JFK',  # Example: Departure airport code
    'destinationLocationCode': 'LAX',  # Example: Arrival airport code
    'departureDate': '2024-11-01',  # Flight departure date
    'adults': 1,  # Number of passengers
    'max': 5  # Limit the number of results
}

# Make the GET request to the API
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    flight_offers = response.json()
    # Example of parsing flight data
for offer in flight_offers['data']:
    price = offer['price']['total']  # Total flight price
    itinerary = offer['itineraries'][0]  # Flight itinerary
    duration = itinerary['duration']  # Flight duration
    segments = itinerary['segments']  # Segments (individual flights)
    
    print(f"Price: ${price}")
    print(f"Duration: {duration}")
    print(f"Segments:")
    for segment in segments:
        departure = segment['departure']
        arrival = segment['arrival']
        airline = segment['carrierCode']
        flight_number = segment['number']
        
        print(f"Flight: {airline}{flight_number}")
        print(f"Departure: {departure['iataCode']} at {departure['at']}")
        print(f"Arrival: {arrival['iataCode']} at {arrival['at']}")
    print('-' * 20)
else:
    print(f"Error: {response.status_code}")