import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN_ENDPOINT="https://api.amadeus.com/v1/security/oauth2/token"
class FlightSearch:
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_API_SECRET"]
        self._token = self._get_new_token()

    def _get_new_token(self):
        # Get a new token from the Amadeus API
        headers = {
        "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=headers, data=data)

        if response.status_code == 200: 
            token_data = response.json()
            print(f"Your token is {token_data['access_token']}")
            print(f"Your token expires in {token_data['expires_in']} seconds")
            return token_data["access_token"]
        else:
            print("Failed to obtain token:")
            print(response.json()) 
            return None
        
    def get_iata_code(self, city):
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {
            "keyword": city,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=TOKEN_ENDPOINT, headers=headers, params=params)
        try:
            response.raise_for_status()
            return response.json()["data"][0]["iataCode"]
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
