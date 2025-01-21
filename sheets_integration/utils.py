import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)


sheet = client.open_by_key("12c5B4A4nYRHA0-9ouKAag44NWr3rgzldQ2bmRTvcrgo").sheet1


data = sheet.get_all_records() 
print(data)

sheet.append_row(["Name", "Email", "Phone"])
