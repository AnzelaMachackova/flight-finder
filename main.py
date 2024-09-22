from data_manager import DataManager
from flight_search import FlightSearch
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def main():
    data_manager = DataManager(GOOGLE_SHEET_ID)
    sheet_data = data_manager.get_data()

    print(sheet_data)
    
    #data_manager.update_iata_code('Paris', 'PAR')
    #update_column(data_manager, 'IATA Code', 'City', 'Frankfurt', 1234)
    flight_search = FlightSearch()
    flight_search.get_iata_code('Paris')


if __name__ == "__main__":
    main()