from django.db import models
from django.contrib.auth.models import User
from apps.transactions.models import Category
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP

# Create your models here.

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    categories = models.ManyToManyField(Category) 
    
    def __str__(self):
        return f"{self.name} (${self.amount})"
    
    def spent_amount(self):
        from apps.transactions.models import Transaction
        total = Transaction.objects.filter(
        user=self.user,
        category__in=self.categories.all(),
        date__range=[self.start_date, self.end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return Decimal(str(total)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        
    def get_category_spending(self, category):
        from apps.transactions.models import Transaction
        return Transaction.objects.filter(
            user=self.user,
            budget=self,
            category=category
        ).aggregate(total=Sum('amount'))['total'] or 0
    
    def remaining_amount(self):
        amount = Decimal(str(self.amount))
        spent = Decimal(str(self.spent_amount()))
        return (amount - spent).quantize(Decimal('0.00'))
    
    