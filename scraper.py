import requests  # Importing the requests library to handle HTTP requests

def get_basic_trends(zip_code):
    # Define the URL of the API endpoint for the GraphQL request
    url = "https://www.gasbuddy.com/graphql"
    
    # GraphQL query to fetch fuel price trends for a given location
    query = {
        "operationName": "LocationBySearchTerm",  # Operation name for the query
        "variables": {
            "search": zip_code  # Passing the ZIP code as a search variable
        },
        "query": """
        query LocationBySearchTerm($search: String!) {
          locationBySearchTerm(search: $search) {  # Search by ZIP code or other location identifier
            trends {  # Requesting the trends for the given location
              areaName  # Area name (e.g., Detroit)
              country  # Country (e.g., USA)
              today  # Today's price for fuel
              todayLow  # Today's lowest price for fuel
            }
          }
        }
        """
    }

    # Headers for the HTTP request to mimic a real browser request
    headers = {
        "Content-Type": "application/json",  # We are sending JSON data
        "User-Agent": "Mozilla/5.0",  # Mimic a real browser user agent
        "Referer": "https://www.gasbuddy.com/",  # Referer header to avoid potential bot detection
        "Origin": "https://www.gasbuddy.com"  # Origin header indicating the source of the request
    }

    # Sending the POST request to the API with the query and headers
    response = requests.post(url, json=query, headers=headers)
    
    # Check if the response status is OK (200)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response into a Python dictionary
        
        # Extract the 'trends' data from the JSON response safely using .get() to avoid KeyError
        trends = data.get("data", {}).get("locationBySearchTerm", {}).get("trends", [])
        
        # Check if trends data was found
        if trends:
            # Loop through each trend in the 'trends' list
            for trend in trends:
                # Print the details of each trend (area name, country, today's price, and lowest price)
                print(f"Area Name: {trend.get('areaName', 'N/A')}")  # Default to 'N/A' if data is missing
                print(f"Country: {trend.get('country', 'N/A')}")  # Default to 'N/A' if data is missing
                print(f"Today's Price: {trend.get('today', 'N/A')}")  # Default to 'N/A' if data is missing
                print(f"Today's Low Price: {trend.get('todayLow', 'N/A')}")  # Default to 'N/A' if data is missing
                print("-" * 40)  # Print a separator line for better readability
        else:
            # If no trends data was found, print a message indicating that
            print("No trends data found.")
    else:
        # If the request failed (non-200 status code), print the error message and status code
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging

# Example usage of the function with a specific ZIP code
zip_code = "48202"  # Replace with the ZIP code you want to check
get_basic_trends(zip_code)  # Call the function with the specified ZIP code
