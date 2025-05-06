from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Category(models.Model):
    INCOME = 'IN'
    EXPENSE = 'EX'
    TYPE_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=EXPENSE)

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    CASH = 'CA'
    CARD = 'CR'
    BANK_TRANSFER = 'BT'
    PAYMENT_METHODS = [
        (CASH, 'Cash'),
        (CARD, 'Card'),
        (BANK_TRANSFER, 'Bank Transfer'),
    ]
    payment_method = models.CharField(
        max_length=2,
        choices=PAYMENT_METHODS,
        default=CARD,
        blank=True
    )
    
    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.category.get_type_display()}: {self.amount} on {self.date}"