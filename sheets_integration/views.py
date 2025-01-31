from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import get_google_sheet
import csv
from django.http import HttpResponse
from .utils import add_google_sheet_data_to_db , fetch_data_from_db
from .models import User


def fetch_from_sheet(request):
    try:
        sheet = get_google_sheet()
        data = sheet.get_all_records()
        return render(request, 'sheets_integration/display_data.html', {'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def save_to_sheet(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            
            if not all([name, email, phone]):
                messages.error(request, 'All fields are required')
                return render(request, 'sheets_integration/add_data.html')
            data = {
                'name': name,
                'email': email,
                'phone': phone
            }
            
            
            sheet = get_google_sheet()
            
            sheet.append_row([name, email, phone])
            
            messages.success(request, 'Data saved successfully!')
            return redirect('save_to_sheet')
            
        except Exception as e:
           
            messages.error(request, f'Error saving data: {str(e)}')
            return render(request, 'sheets_integration/add_data.html')
    
    return render(request, 'sheets_integration/add_data.html')


def download_db_data(request):
    try:
        
        records = User.objects.all()

        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="database_data.csv"'

        
        fieldnames = ['name', 'email', 'phone']

       
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({
                'name': record.name,
                'email': record.email,
                'phone': record.phone
            })

        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        try:
            
            csv_file = request.FILES['csv_file']

            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Invalid file type. Please upload a CSV file.')
                return render(request, 'sheets_integration/upload_csv.html')

            
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            
            sheet = get_google_sheet()
            headers = sheet.row_values(1)
            if set(reader.fieldnames) != set(headers):
                messages.error(request, 'The CSV headers do not match the Google Sheet headers.')
                return render(request, 'sheets_integration/upload_csv.html')

            
            for row in reader:
                row_values = [row.get(header, '') for header in headers]
                sheet.append_row(row_values)

            messages.success(request, 'CSV data uploaded successfully!')
            return redirect('show_data_view')
        except Exception as e:
            messages.error(request, f'Error processing the file: {str(e)}')
            return render(request, 'sheets_integration/upload_csv.html')

    return render(request, 'sheets_integration/upload_csv.html')

def show_data_view(request):
    
    data = fetch_data_from_db()

    
    context = {'data': data}
    return render(request, 'sheets_integration/display_data.html', context)


def sync_google_sheet(request):
    try:
        add_google_sheet_data_to_db()
        messages.success(request, "Google Sheet data has been synced successfully.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('show_data_view') 