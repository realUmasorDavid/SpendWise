from django.shortcuts import render, redirect, get_object_or_404
from apps.transactions.models import *

# Create your views here.

def transaction_history(request):
    
    transaction = Transaction.objects.filter(user=request.user)
    
    context = {
        'transaction': transaction,
        'current_path': request.path,
    }
    
    return render(request, 'reports/history.html', context)