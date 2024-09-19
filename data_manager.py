import gspread
from google.oauth2 import service_account

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, sheet_id):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=scope)
        client = gspread.authorize(credentials)
        self.sheet = client.open_by_key(sheet_id).sheet1

    def get_data(self):
        return self.sheet.get_all_records()

    def update_column(self, column_to_update, column_condition, condition_value, new_value):
        records = self.get_data()
        headers = self.sheet.row_values(1)
        index_to_update = headers.index(column_to_update) + 1  
        #index_condition = headers.index(column_condition) + 1

        for i, record in enumerate(records, start=2):
            if record[column_condition] == condition_value:
                print(f"Updating row {i} with value {new_value}.")
                self.sheet.update_cell(i, index_to_update, new_value)
            else:
                print(f"City {condition_value} not found.")
    

    def update_iata_code(self, city, iata_code):
        records = self.get_data()
        headers = self.sheet.row_values(1)
        index_to_update = headers.index('IATA Code') + 1

        for i, record in enumerate(records, start=2):
            if record['City'] == city:
                print(f"Updating row {i} with value {iata_code}")
                self.sheet.update_cell(i, index_to_update, iata_code)
                break
