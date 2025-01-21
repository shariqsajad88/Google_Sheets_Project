import os
from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet():
    credentials_path = os.path.join(settings.BASE_DIR, 'sheets_integration/credentials.json')
    
    
    print(f"Looking for credentials at: {credentials_path}")
    print(f"File exists: {os.path.exists(credentials_path)}")
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("12c5B4A4nYRHA0-9ouKAag44NWr3rgzldQ2bmRTvcrgo").sheet1



def save_to_sheet(data):
    try:
        print(f"Data received by save_to_sheet: {data}")
        sheet = get_google_sheet()
        print(f"Google Sheet object: {sheet}")
        
        # Append data
        sheet.append_row([data.get('name'), data.get('email'), data.get('phone')])
        return True, "Data saved successfully."
    except Exception as e:
        print(f"Error in save_to_sheet: {str(e)}")
        return False, f"An error occurred: {str(e)}"
