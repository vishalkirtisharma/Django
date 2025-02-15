from django.db import models

"""
Models for the Expenses Tracker application.
Defines the database schema and business logic for expenses.
"""

class ExpensesModel(models.Model):
    """
    Model representing an expense entry.
    
    Attributes:
        name: Name/description of the expense (max 100 chars)
        amount: Amount of the expense in whole numbers
        category: Category of the expense (max 100 chars)
        date: Date when the expense was recorded (auto-set to current date)
    """
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)


    class Meta:
        """
        Metadata for the ExpensesModel.
        
        Attributes:
            verbose_name: Singular name for the model
            verbose_name_plural: Plural name for the model
        """
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"


    def __str__(self):
        """
        String representation of the expense.
        
        Returns:
            Formatted string containing expense details
        """
        return self.name + " - " + str(self.amount) + " - " + self.category + " - " + str(self.date)
