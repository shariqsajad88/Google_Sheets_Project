import os
from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet():
    credentials_path = os.path.join(settings.BASE_DIR, 'sheets_integration/credentials.json')
    
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("12c5B4A4nYRHA0-9ouKAag44NWr3rgzldQ2bmRTvcrgo").sheet1

def append_to_sheet(data):
   
    try:
        sheet = get_google_sheet()
        
        
        
        headers = sheet.row_values(1)
        
        
        
        row_values = [str(data.get(header, '')) for header in headers]
        
        
        
        sheet.append_row(row_values)
        
        
        return True, "Data saved successfully"
    except Exception as e:
        
        return False, f"Error saving data: {str(e)}"