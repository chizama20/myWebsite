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
              todayLow-
              
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
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "locationBySearchTerm" in data["data"]:
            trends = data["data"]["locationBySearchTerm"].get("trends", [])
            if trends:
                for trend in trends:
                    print(f"Area Name: {trend.get('areaName')}")
                    print(f"Country: {trend.get('country')}")
                    print(f"Today's Price: {trend.get('today')}")
                    print(f"Today's Low Price: {trend.get('todayLow')}")
                    print("-" * 40)
            else:
                print("No trends data found.")
        else:
            print("No data found for the given ZIP code.")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  


zip_code = "48202" 
get_basic_trends(zip_code)
