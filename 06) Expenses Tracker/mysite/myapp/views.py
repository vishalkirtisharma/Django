from django.shortcuts import render, redirect
from . import forms, models
from django.db.models import Sum
import datetime
"""
Views for the Expenses Tracker application.
Handles displaying, adding, editing, and deleting expenses.
"""


def index(request):
    """
    Main view for displaying expenses and handling new expense creation.
    
    Args:
        request: HttpRequest object containing metadata about the request
        
    Returns:
        Rendered template with:
        - form: Expense form instance
        - expenses: List of all expenses
        - total_expenses: Sum of all expense amounts
    """
    form = forms.ExpensesForm()

    # Handle form submission
    if request.method == 'POST':
        form = forms.ExpensesForm(request.POST)
        if form.is_valid():
            form.save()

    # Get all expenses and calculate total
    expenses = models.ExpensesModel.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))
    
    # Logic to calculate 365 ezpenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = models.ExpensesModel.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))


    # Logic to calculate last ezpenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = models.ExpensesModel.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

    # Logic to calculate last ezpenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = models.ExpensesModel.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    daily_sum = models.ExpensesModel.objects.filter().values('date').annotate(sum=Sum('amount'))
    
    
    categorical_sum = models.ExpensesModel.objects.filter().values('category').annotate(sum=Sum('amount'))
    


    return render(request, 'myapp/index.html', {
        'form': form,
        'expenses': expenses,
        'total_expenses': total_expenses['amount__sum'],
        'yearly_sum': yearly_sum['amount__sum'],
        'monthly_sum': monthly_sum['amount__sum'],
        'weekly_sum': weekly_sum['amount__sum'],
        'daily_sum': daily_sum,
        'categorical_sum': categorical_sum,
    })



def edit(request, id):
    """
    View for editing an existing expense.
    
    Args:
        request: HttpRequest object
        id: ID of the expense to edit
        
    Returns:
        Rendered edit template with form pre-populated with expense data
        or redirects to index after successful update
    """
    expense = models.ExpensesModel.objects.get(id=id)
    form = forms.ExpensesForm(instance=expense)

    # Handle form submission
    if request.method == 'POST':
        form = forms.ExpensesForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')
            
    return render(request, 'myapp/edit.html', {'form': form})



def delete(request, id):
    """
    View for deleting an expense.
    
    Args:
        request: HttpRequest object
        id: ID of the expense to delete
        
    Returns:
        Redirects to index page after deletion
    """
    if request.method == 'POST' and 'delete' in request.POST:
        expense = models.ExpensesModel.objects.get(id=id)
        expense.delete()
    return redirect('myapp:index')
