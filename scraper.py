import requests

def get_basic_trends(zip_code):
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
              # Remove any additional fields for now
            }
          }
        }
        """
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.gasbuddy.com/",
        "Origin": "https://www.gasbuddy.com"
    }

    response = requests.post(url, json=query, headers=headers)
    
    # Print the raw response for debugging
    if response.status_code == 200:
        data = response.json()
        print(data)  # Print the entire response for debugging
    else:
        print(response.text)  # Print the raw response text

# Example usage:
zip_code = "90210"  # Enter your ZIP code
get_basic_trends(zip_code)
