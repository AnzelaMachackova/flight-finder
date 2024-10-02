from google.cloud import bigquery
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import pytz

load_dotenv()

project_id = os.getenv('BIGQUERY_PROJECT_ID')
dataset_id = os.getenv('BIGQUERY_DATASET_ID')
city_table_id = os.getenv('BIGQUERY_CITY_TABLE_ID')
flight_table_id = os.getenv('BIGQUERY_FLIGHT_TABLE_ID')
api_key = os.getenv('AMADEUS_API_KEY')
api_secret = os.getenv('AMADEUS_API_SECRET')

def fetch_iata_codes(project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    query = f"""
        SELECT `iata_code` FROM `{dataset_id}.{table_id}`
    """
    
    query_job = client.query(query)
    results = query_job.result()  
    iata_codes = [row['iata_code'] for row in results]
    return iata_codes

def get_lowest_price_flight_details(api_key, api_secret, origin, destination, departure_date):
    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    auth_payload = {
        "client_id": api_key,
        "client_secret": api_secret,
        "grant_type": "client_credentials"
    }
    auth_response = requests.post(auth_url, data=auth_payload)
    access_token = auth_response.json()['access_token']
    headers = {"Authorization": f"Bearer {access_token}"}
    base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date.strftime('%Y-%m-%d'),
        "adults": 1
    }

    response = requests.get(base_url, headers=headers, params=params)
    flights = response.json().get('data', [])

    lowest_price = float('inf')
    best_flight = None
    for flight in flights:
        price = float(flight['price']['total'])
        if flight['price']['currency'] == 'EUR' and price < lowest_price:
            lowest_price = price
            best_flight = flight
    print(f"Lowest price for {destination} is {lowest_price} EUR")

    if best_flight:
        aircraft_code = best_flight['itineraries'][0]['segments'][0]['aircraft']['code']
        duration = best_flight['itineraries'][0]['duration']
        dates = best_flight['itineraries'][0]['segments'][0]['departure']['at']
        print(f"Flight details: Aircraft code: {aircraft_code}, Duration: {duration}, Dates: {dates}")
        return {
            "price": lowest_price,
            "aircraft_code": aircraft_code,
            "duration": duration,
            "dates": dates
        }
    return None

def update_bigquery_table(project_id, dataset_id, table_id, destination, flight_details):
    client = bigquery.Client(project=project_id)
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref) 

    timestamp = datetime.now(pytz.timezone('UTC')).isoformat()

    rows_to_insert = [
        {
            "iata_code": destination,
            "lowest_price": flight_details['price'],
            "aircraft_code": flight_details['aircraft_code'],
            "duration": flight_details['duration'],
            "flight_dates": flight_details['dates'],
            "insert_timestamp": timestamp
        }
    ]

    errors = client.insert_rows_json(table, rows_to_insert) 
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

def main():
    origin = 'PRG'  
    departure_date = datetime.now() + timedelta(days=7)  # Departure date to 7 days from today

    # Fetching destination codes from BigQuery
    destinations = fetch_iata_codes(project_id, dataset_id, city_table_id)
    print(f"Fetching flight details for {len(destinations)} destinations...")
    for destination in destinations:
        flight_details = get_lowest_price_flight_details(api_key, api_secret, origin, destination, departure_date)
        if flight_details:
            # Update BigQuery table with the fetched flight details
            update_bigquery_table(project_id, dataset_id, flight_table_id, destination, flight_details)
        else:
            print(f"No suitable flights found for destination {destination}")

if __name__ == '__main__':
    main()
