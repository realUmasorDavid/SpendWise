from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.transactions.models import *
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError

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
    budget = get_object_or_404(Budget, pk=pk, user=request.user)  # Added user check for security
    
    if request.method == 'POST':
        try:
            # Get and validate form data
            new_name = request.POST.get('name', '').strip()
            new_amount = request.POST.get('amount', '').strip()
            new_start_date = request.POST.get('start_date', '').strip()
            new_end_date = request.POST.get('end_date', '').strip()
            new_categories = request.POST.getlist('categories', [])
            
            # Validate required fields
            if not new_name:
                raise ValidationError("Name is required.")
            if not new_amount:
                raise ValidationError("Amount is required.")
            if not new_start_date:
                raise ValidationError("Start date is required.")
            if not new_end_date:
                raise ValidationError("End date is required.")
            if not new_categories:
                raise ValidationError("At least one category is required.")

            # Convert and validate amount
            try:
                amount_decimal = Decimal(new_amount)
                if amount_decimal <= 0:
                    raise ValidationError("Amount must be positive.")
            except:
                raise ValidationError("Invalid amount format.")

            # Update budget
            budget.name = new_name
            budget.amount = amount_decimal
            budget.start_date = new_start_date
            budget.end_date = new_end_date
            
            # Clear and set categories
            budget.categories.clear()
            for category_id in new_categories:
                category = get_object_or_404(Category, pk=category_id, user=request.user)
                budget.categories.add(category)
            
            budget.save()
            messages.success(request, "Budget updated successfully!")
            return redirect('budget_list')

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    # Get all user's expense categories for the form
    categories = Category.objects.filter(user=request.user, type='EX')
    
    return render(request, 'budgets/budget_list.html', {
        'budget': budget,
        'categories': categories,
        'selected_categories': budget.categories.values_list('id', flat=True)
    })
    
def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    categories = Category.objects.filter(user=request.user, type='EX')  # Only expense categories
    
    if request.method == 'POST':
        new_name = request.POST.get('name', '')
        new_start_date = request.POST.get('start_date', '')
        new_end_date = request.POST.get('end_date', '')

        budget.name = new_name
        budget.start_date = new_start_date
        budget.end_date = new_end_date
        budget.save()

        messages.success(request, "Budget updated successfully!")
        return redirect('budget_list')
        
    context = {
        'budget': budget,
        'categories': categories,
    }
    
    return render(request, 'budgets/budget_edit.html', context)

def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        budget.delete()
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