from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.transactions.models import *

# Create your views here.

def budget(request):
    category = Category.objects.filter(user=request.user, type='EX')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        categories = request.POST.getlist('categories')

        budget = Budget.objects.create(
            user=request.user,
            name=name,
            amount=amount,
            start_date=start_date,
            end_date=end_date
        )
        
        budget.categories.set(categories)
        budget.save()
    
    context = {
        'category': category,
    }
    return render(request, 'budgets/budget.html', context)

def list(request):
    budgets = Budget.objects.filter(user=request.user)
    
    context = {
        'budgets': budgets,
    }
    return render(request, 'budgets/budget_list.html', context)

def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk)

    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_amount = request.POST.get('amount')
        new_start_date = request.POST.get('start_date')
        new_end_date = request.POST.get('end_date')
        new_categories = request.POST.getlist('categories')
        
        # Validate form data
        if not new_name:
            return render(request, 'budgets/budget_list.html', {"budget": budget, "error": "Name is required."})

        if not new_amount:
            return render(request, 'budgets/budget_list.html', {"budget": budget, "error": "Amount is required."})

        if not new_start_date:
            return render(request, 'budgets/budget_list.html', {"budget": budget, "error": "Start Date is required."})
        
        if not new_end_date:
            return render(request, 'budgets/budget_list.html', {"budget": budget, "error": "End Date is required."})
        
        if not new_categories:
            return render(request, 'budgets/budget_list.html', {"budget": budget, "error": "Category is required."})

        budget.name = new_name
        budget.amount = new_amount
        budget.start_date = new_start_date
        budget.end_date = new_end_date
        budget.categories = new_categories
        budget.save()

        return redirect('budget_list')
    return render(request, 'budgets/budget_list.html', {'budget': budget})

def budget_delete(request, pk):
    notes = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        notes.delete()
        return redirect('budget_list')
    return render(request, 'budgets/budget_list.html', {'budget': budget})

def update_spending(request):
    if request.method == 'POST':
        budget_id = request.POST.get('budget_id')
        category_id = request.POST.get('category_id')
        amount = request.POST.get('amount')
        
        # Create or update transaction
        transaction, created = Transaction.objects.update_or_create(
            user=request.user,
            budget_id=budget_id,
            category_id=category_id,
            defaults={
                'amount': amount,
                'name': 'Manual Budget Adjustment',
                'date': timezone.now().date()
            }
        )
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)