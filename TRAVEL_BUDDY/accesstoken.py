import requests

api_key = 'jyjjgRUInHLxGGeE490AJjG63JMXkgju'
api_secret = '7VNymbmwuynV7cip'

url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': 'client_credentials',
    'client_id': api_key,
    'client_secret': api_secret
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print(f'Access token: {access_token}')
else:
    print(f"Failed to get access token: {response.status_code}")
