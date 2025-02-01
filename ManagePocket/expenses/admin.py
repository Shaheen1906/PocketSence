from django.contrib import admin
from .models import  Student, Group, Category, Expense, Settlement

# Register your models here
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'college', 'semester', 'default_payment_method', 'upi_id')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'created_at')
    filter_horizontal = ('members',)  # For easier selection of members

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id','amount', 'category', 'split_type', 'date', 'paid_by', 'group')

@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('id','expense', 'payer', 'payee', 'amount', 'payment_status', 'due_date')