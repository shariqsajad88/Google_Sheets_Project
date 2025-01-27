import os
from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .models import User



def get_google_sheet():
    credentials_path = os.path.join(settings.BASE_DIR, 'sheets_integration/credentials.json')
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    return client.open_by_key("12c5B4A4nYRHA0-9ouKAag44NWr3rgzldQ2bmRTvcrgo").sheet1

def add_google_sheet_data_to_db():
    try:
        sheet = get_google_sheet()
        records = sheet.get_all_records()

        for record in records:
            
            if not User.objects.filter(email=record.get('Email')).exists():
                User.objects.create(
                    name=record.get('Name'),
                    email=record.get('Email'),
                    phone=record.get('Phone')
                )
        print("Data insertion completed.")
    except Exception as e:
        print(f"Error: {e}")


def append_to_sheet(data):
   
    try:
        sheet = get_google_sheet()
        
        headers = sheet.row_values(1)
        
        row_values = [str(data.get(header, '')) for header in headers]
        
        sheet.append_row(row_values)
        
        
        return True, "Data saved successfully"
    except Exception as e:
        
        return False, f"Error saving data: {str(e)}"
    
def fetch_data_from_db():
    records = User.objects.all()

    seen_emails = set()
    unique_records = []

    for record in records:
        if record.email not in seen_emails:
            seen_emails.add(record.email)
            unique_records.append({
                "name": record.name,
                "email": record.email,
                "phone": record.phone
            })

    return unique_records
    