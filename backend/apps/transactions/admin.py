from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'type')
    search_fields = ['name', 'user']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'category', 'amount', 'date', 'created_at')
    search_fields = ['name', 'user']
    list_filter = ['category']
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)