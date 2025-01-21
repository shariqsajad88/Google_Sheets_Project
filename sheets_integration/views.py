from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .utils import get_google_sheet, save_to_sheet
import json

def fetch_from_sheet(request):
    try:
        sheet = get_google_sheet()
        data = sheet.get_all_records()
        return render(request, 'sheets_integration/display_data.html', {'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def add_data_form(request):
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone')
        }

        if not all(data.values()):
            return render(request, 'sheets_integration/add_data.html', {
                'error': 'All fields are required.'
            })

        success, message = save_to_sheet(data)
        if success:
            return redirect('fetch_from_sheet')
        else:
            return render(request, 'sheets_integration/add_data.html', {'error': message})

    return render(request, 'sheets_integration/add_data.html')
