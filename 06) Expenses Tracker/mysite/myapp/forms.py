from django import forms
from . import models

class ExpensesForm(forms.ModelForm):
    """
    Form for creating and editing expenses.
    
    Inherits from ModelForm to automatically generate form fields
    based on the ExpensesModel.
    """
    
    class Meta:
        model = models.ExpensesModel
        fields = ('name', 'amount', 'category')
        """
        Meta class defining the model and fields to include in the form.
        
        Attributes:
            model: The model class to use for the form
            fields: Tuple of field names to include in the form
        """
