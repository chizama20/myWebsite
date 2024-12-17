import requests

# Replace this with your Skyscanner API Key
API_KEY = 'YOUR_SKYSCANNER_API_KEY'

# Skyscanner API endpoint for browsing quotes (flights)
SKYSCANNER_URL = 'https://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US/{}/{}/{}'

# Function to get flight offers
def find_flights(origin, destination, departure_date):
    url = SKYSCANNER_URL.format(
        'US',  # Country code (US is for the United States)
        origin,  # e.g. 'SFO-sky' for San Francisco
        destination,  # e.g. 'ORD-sky' for Chicago O'Hare
        departure_date  # Format: 'YYYY-MM-DD' (e.g. '2024-11-01')
    )
    
    # Set headers with your API Key
    headers = {
        'x-rapidapi-key': API_KEY
    }

    # Make the request to the Skyscanner API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        flight_data = response.json()
        return flight_data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def main():
    print("Flight Finder\n")
    
    # User input for flight search
    origin = input("Enter origin airport (e.g., SFO): ").strip()
    destination = input("Enter destination airport (e.g., ORD): ").strip()
    departure_date = input("Enter departure date (YYYY-MM-DD): ").strip()

    # Find flights
    flight_data = find_flights(origin, destination, departure_date)
    
    if flight_data:
        # Display the flight offers
        if 'Quotes' in flight_data:
            print(f"\nFlight search results from {origin} to {destination} on {departure_date}:\n")
            for flight in flight_data['Quotes']:
                price = flight.get('MinPrice', 'N/A')
                departure = flight.get('OutboundLeg', {}).get('DepartureDate', 'N/A')
                carrier_ids = flight.get('OutboundLeg', {}).get('CarrierIds', [])
                print(f"Price: {price} USD | Departure: {departure} | Carrier IDs: {carrier_ids}")
        else:
            print("No flights found.")
    else:
        print("Failed to retrieve flight data.")

if __name__ == '__main__':
    main()
