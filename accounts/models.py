from django.contrib.auth.models import AbstractUser
from django.db import models

from MoneyManager import settings


class User(AbstractUser):
    fullname = models.CharField(max_length=75)

    REQUIRED_FIELDS = ['email']  # Optionally add other fields as required

class UserExpenses(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=50,
        choices=[
            ('food', 'Food'),
            ('transportation', 'Transportation'),
            ('utilities', 'Utilities'),
            ('entertainment', 'Entertainment'),
            ('other', 'Other')
        ],
    )
    date = models.DateField()
    
    # created_at field helps you keep a timestamp of when the record was created.
    created_at = models.DateTimeField(auto_now_add=True)
    # This updated_at allows you to monitor changes over time and know the latest state of your data.
    updated_at = models.DateTimeField(auto_now=True)

# Monthly Income model
class MonthlyIncome(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    month = models.IntegerField()  # 1 = January, 2 = February, etc.
    year = models.IntegerField()
    income = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # Prevent duplicate entries
        unique_together = ('user', 'month', 'year')

# Budget per category model
class CategoryBudget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    category = models.CharField(
        max_length=50,
        choices=[
            ('food', 'Food'),
            ('transportation', 'Transportation'),
            ('utilities', 'Utilities'),
            ('entertainment', 'Entertainment'),
            ('other', 'Other'),
        ]
    )
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()  # Add month field to keep track of the budget month
    year = models.IntegerField()

# Monthly Savings model
class MonthlySavings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    savings = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'month', 'year')
