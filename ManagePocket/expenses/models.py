from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField

class Student(AbstractUser):
    college = models.CharField(max_length=100)
    semester = models.IntegerField(blank=True, null=True)
    default_payment_method = models.CharField(max_length=50, blank=True, null=True)
    upi_id = models.CharField(max_length=50, blank=True, null=True)

    # Add unique related_name attributes to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_groups',  # Unique related_name
        blank=True,
        help_text='The groups this student belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_user_permissions',  # Unique related_name
        blank=True,
        help_text='Specific permissions for this student.',
        verbose_name='user permissions',
    )
    def __str__(self):
        return f"{self.username}"

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Student, related_name='group_members')  # Unique related_name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Expense(models.Model):
    SPLIT_TYPES = [
        ('EQUAL', 'Equal'),
        ('UNEQUAL', 'Unequal'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    split_type = models.CharField(max_length=10, choices=SPLIT_TYPES)
    split_details = JSONField(default=dict)
    date = models.DateField()
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    paid_by = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='expenses_paid')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.category}"

class Settlement(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    payer = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='settlements_paid')
    payee = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='settlements_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    settlement_method = models.CharField(max_length=50)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.payer.username} owes {self.payee.username} ₹{self.amount}"
