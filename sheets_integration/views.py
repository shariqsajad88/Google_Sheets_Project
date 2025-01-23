from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import get_google_sheet, append_to_sheet

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