from data_manager import DataManager
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

def main():
    data_manager = DataManager(GOOGLE_SHEET_ID)
    sheet_data = data_manager.get_data()

    print(sheet_data)
    
    # Function to update a column in the sheet based on a condition
    def update_column(data_manager, column_to_update, column_condition, condition_value, new_value):
        records = data_manager.get_data()
        sheet = data_manager.sheet
        headers = sheet.row_values(1)
        index_to_update = headers.index(column_to_update) + 1  
        # index_condition = headers.index(column_condition) + 1

        for i, record in enumerate(records, start=2):  # start=2 because rows in gsheets are 1-based and the first row is headers
            if record[column_condition] == condition_value:
                print(f"Updating row {i} with value {new_value}")
                sheet.update_cell(i, index_to_update, new_value)

    update_column(data_manager, 'IATA Code', 'City', 'Frankfurt', 1234)

if __name__ == "__main__":
    main()