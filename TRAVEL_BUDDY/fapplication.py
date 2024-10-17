import os
from flask import Flask, request, jsonify
import requests
import openai

app = Flask(__name__)

# Set your Amadeus API access token
access_token = 'BLMUuXruR4tIXGywdos16AESDrG7'
url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
headers = {
    'Authorization': f'Bearer {access_token}'
}

openai.api_key = os.getenv('OPENAI_API_KEY')

def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, world!"}]
        )
        print("OpenAI API is working:", response.choices[0].message.content)
    except Exception as e:
        print("Error with OpenAI API:", str(e))

test_openai_api()
 

@app.route('/')
def home():
    return "Welcome to the Flight Finder AI!"

@app.route('/find-flights', methods=['POST'])
def find_flights():
    user_input = request.json.get('query')
    # Process user input using OpenAI to extract relevant details
    flight_details = process_user_input(user_input)

    if flight_details:
        params = {
            'originLocationCode': flight_details['origin'],
            'destinationLocationCode': flight_details['destination'],
            'departureDate': flight_details['date'],
            'adults': 1,
            'max': 5
        }

        # Make the GET request to the Amadeus API
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            flight_offers = response.json()
            return jsonify(parse_flight_data(flight_offers))
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Amadeus API error: {str(e)}"}), 500
    else:
        return jsonify({"error": "Could not process user input."}), 400

def process_user_input(user_input):
    if not user_input:
        print("No user input provided.")
        return None

    # Use OpenAI to extract flight details
    prompt = f"Extract flight details (origin, destination, date) from this request: '{user_input}'."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if you have access
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        
        # Log the full response for debugging
        print("OpenAI response:", response)

        response_text = response.choices[0].message['content'].strip()
        print("Response text:", response_text)  # Log the response text

        # Parse the response to extract details
        details = {}
        # Example: "From JFK to LAX on 2024-11-01"
        parts = response_text.split(" ")
        
        # Ensure there are enough parts to avoid index errors
        if len(parts) >= 6:
            details['origin'] = parts[1]  # Adjust based on your expected response format
            details['destination'] = parts[3]
            details['date'] = parts[5]
            return details
        else:
            print("Response did not contain enough parts to extract details.")
            return None
    except Exception as e:
        print(f"Error processing user input: {e}")
        return None

def parse_flight_data(flight_offers):
    # Parse flight data from the Amadeus response
    results = []
    for offer in flight_offers['data']:
        price = offer['price']['total']
        itinerary = offer['itineraries'][0]
        duration = itinerary['duration']
        segments = itinerary['segments']
        
        flight_info = {
            'price': price,
            'duration': duration,
            'segments': []
        }

        for segment in segments:
            departure = segment['departure']
            arrival = segment['arrival']
            airline = segment['carrierCode']
            flight_number = segment['number']
            
            flight_info['segments'].append({
                'flight': f"{airline} {flight_number}",
                'departure': f"{departure['iataCode']} at {departure['at']}",
                'arrival': f"{arrival['iataCode']} at {arrival['at']}"
            })
        
        results.append(flight_info)
    
    return results

if __name__ == '__main__':
    app.run(debug=True)
