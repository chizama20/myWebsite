import requests

def get_basic_trends(zip_code):
    # Define the URL and GraphQL query
    url = "https://www.gasbuddy.com/graphql"
    
    query = {
        "operationName": "LocationBySearchTerm",
        "variables": {
            "search": zip_code
        },
        "query": """
        query LocationBySearchTerm($search: String!) {
          locationBySearchTerm(search: $search) {
            trends {
              areaName
              country
              today
              todayLow
            }
          }
        }
        """
    }

    # Headers for the HTTP request
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.gasbuddy.com/",
        "Origin": "https://www.gasbuddy.com"
    }

    # Make the POST request
    response = requests.post(url, json=query, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Safely access trends data
        trends = data.get("data", {}).get("locationBySearchTerm", {}).get("trends", [])
        
        if trends:
            for trend in trends:
                print(f"Area Name: {trend.get('areaName', 'N/A')}")
                print(f"Country: {trend.get('country', 'N/A')}")
                print(f"Today's Price: {trend.get('today', 'N/A')}")
                print(f"Today's Low Price: {trend.get('todayLow', 'N/A')}")
                print("-" * 40)
        else:
            print("No trends data found.")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

# Call the function with a ZIP code
zip_code = "48202" 
get_basic_trends(zip_code)
