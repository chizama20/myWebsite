import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = 'https://www.example.com/fuel-prices'  # Replace with the actual URL

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the specific element containing fuel prices
    # You need to inspect the page structure to find the correct tag and class
    fuel_prices = soup.find_all('div', class_='price')  # Adjust this to match the site's structure
    
    # Loop through and print the fuel prices
    for price in fuel_prices:
        print(price.text.strip())
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
