import requests
from datetime import datetime
from tabulate import tabulate

def fetch_trends(zip_code, url, headers):
    query = {
        "operationName": "LocationBySearchTerm",
        "variables": {"search": zip_code},
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
    try:
        response = requests.post(url, json=query, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("locationBySearchTerm", {}).get("trends", [])
    except Exception as e:
        print(f"Error fetching trends: {e}")
        return []

def display_trends_table(trends, current_date):
    if trends:
        table = [
            [trend.get('areaName', 'N/A'), trend.get('country', 'N/A'),
             trend.get('today', 'N/A'), trend.get('todayLow', 'N/A')]
            for trend in trends
        ]
        print(f"Data fetched on: {current_date}")
        print(tabulate(table, headers=["Area Name", "Country", "Today's Price", "Today's Low Price"]))
    else:
        print("No trends data found.")

def get_basic_trends(zip_code, date_format="%Y-%m-%d %H:%M:%S"):
    url = "https://www.gasbuddy.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    current_date = datetime.now().strftime(date_format)
    trends = fetch_trends(zip_code, url, headers)
    display_trends_table(trends, current_date)

# Example usage
get_basic_trends("48202")
