from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from apps.users.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
# Create your views here.

@login_required
def dashboard(request):
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    first_day = datetime(current_year, current_month, 1).date()
    last_day = datetime(
        current_year, 
        current_month + 1 if current_month < 12 else 1,
        1
    ).date() - timedelta(days=1)
    
    prev_month = now.replace(day=1) - timedelta(days=1)
    prev_first_day = prev_month.replace(day=1).date()
    prev_last_day = prev_month.date()
    
    monthly_transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=first_day,
        date__lte=last_day
    )
    
    monthly_income_total = Decimal(str(monthly_transactions.filter(
        category__type='IN'
    ).aggregate(total=Sum('amount'))['total'] or 0)).quantize(Decimal('0.00'))

    monthly_expense_total = Decimal(str(monthly_transactions.filter(
        category__type='EX'
    ).aggregate(total=Sum('amount'))['total'] or 0)).quantize(Decimal('0.00'))
    
    profile = get_object_or_404(Profile, user=request.user)
    
    income_total = Decimal(str(Transaction.objects.filter(
        user=request.user,
        category__type='IN'
    ).aggregate(total=Sum('amount'))['total'] or 0)).quantize(Decimal('0.00'))

    expense_total = Decimal(str(Transaction.objects.filter(
        user=request.user,
        category__type='EX'
    ).aggregate(total=Sum('amount'))['total'] or 0)).quantize(Decimal('0.00'))

    starting_balance = Decimal(str(profile.starting_balance or 0)).quantize(Decimal('0.00'))
    
    available_balance = (starting_balance + (income_total - expense_total)).quantize(Decimal('0.00'))
    
    prev_transactions = Transaction.objects.filter(
        user=request.user,
        date__range=(prev_first_day, prev_last_day)
    )
    prev_income = Decimal(str(prev_transactions.filter(category__type='IN').aggregate(Sum('amount'))['amount__sum'] or 0)).quantize(Decimal('0.00'))
    prev_expense = Decimal(str(prev_transactions.filter(category__type='EX').aggregate(Sum('amount'))['amount__sum'] or 0)).quantize(Decimal('0.00'))
    
    # Calculate changes (already in Decimal)
    income_change = monthly_income_total - prev_income
    expense_change = monthly_expense_total - prev_expense
    balance_change = (income_change - expense_change).quantize(Decimal('0.00'))
    
    # Percentage changes (rounded to 2dp)
    def get_change(current, previous):
        if previous == 0:
            return 100.00  # Return as float with 2 decimal places
        return round(((current - previous) / previous) * 100, 2)
    
    percentage_income_change = get_change(monthly_income_total, prev_income)
    percentage_expense_change = get_change(monthly_expense_total, prev_expense)
    percentage_balance_change = get_change(available_balance, starting_balance)
    
    current_month = timezone.now().strftime("%B %Y")
    
    context = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'full_name': f"{request.user.first_name} {request.user.last_name}",
        'avatar': request.user.profile.avatar.url if request.user.profile.avatar else None,
        'transactions': Transaction.objects.filter(user=request.user),
        'income_total': income_total,
        'expense_total': expense_total,
        'monthly_income_total': monthly_income_total,
        'monthly_expense_total': monthly_expense_total,
        'available_balance': available_balance,
        'income_change': income_change,
        'expense_change': expense_change,
        'balance_change': balance_change,
        'percentage_income_change': percentage_income_change,
        'percentage_expense_change': percentage_expense_change,
        'percentage_balance_change': percentage_balance_change,
        'current_month': current_month,
    }
    
    return render(request, 'transactions/dashboard.html', context)

def create_transaction(request):
    if request.method == 'POST':
        try:
            category_id = request.POST['category']
                
            category = Category.objects.get(id=category_id, user=request.user)
            
            name = request.POST.get('name')
            
            amount = request.POST.get('amount')
                
            date_str = request.POST.get('date')
            
            transaction_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                
            Transaction.objects.create(
                user=request.user,
                name = name,
                category=category,
                amount=amount,
                date=transaction_date,
                description=request.POST.get('description', '')
            )
            
            messages.success(request, 'Transaction created successfully!')
            return redirect('dashboard')
            
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category selected')
            
    context = {
        'categories': Category.objects.filter(user=request.user),
    }
    return render(request, 'transactions/create.html', context)

def create_category(request):
    
    context = {
        'categories': Category.objects.filter(user=request.user),
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        
        if name and type:
            Category.objects.create(
                user=request.user,
                name=name,
                type=type
            )
            messages.success(request, 'Category created successfully!')
            return redirect('create_category')
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'transactions/category.html', context)