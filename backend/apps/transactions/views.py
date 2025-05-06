from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *

# Create your views here.

@login_required
def dashboard(request):
    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'full_name': f"{request.user.first_name} {request.user.last_name}",
        'avatar': request.user.profile.avatar.url if request.user.profile.avatar else None,
    }
    
    return render(request, 'transactions/dashboard.html', context)

def create_transaction(request):
    # if request.method == 'POST':
    #     amount = request.POST['id_amount']
    #     category = request.POST['id_category']
    #     pass 
    
    return render(request, 'transactions/create.html')