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

    def push_data(self, data):
        self.sheet.append_row(data)

    def update_data(self, row, column, value):
        self.sheet.update_cell(row, column, value)  