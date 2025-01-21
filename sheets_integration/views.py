from django.http import JsonResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from django.conf import settings

def fetch_from_sheet(request):
    # Get the absolute path to credentials file
    credentials_path = os.path.join(settings.BASE_DIR, 'sheets_integration/credentials.json')
    
    # Debug print to see where it's looking for the file
    print(f"Looking for credentials at: {credentials_path}")
    
    # Check if file exists
    if not os.path.exists(credentials_path):
        return JsonResponse({
            'error': f'Credentials file not found at {credentials_path}'
        }, status=404)
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("12c5B4A4nYRHA0-9ouKAag44NWr3rgzldQ2bmRTvcrgo").sheet1

    data = sheet.get_all_records()
    return JsonResponse(data, safe=False)