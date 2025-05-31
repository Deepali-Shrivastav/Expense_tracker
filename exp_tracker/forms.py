from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the username similarity validator
        self.fields['password1'].validators = [v for v in self.fields['password1'].validators 
                   

class ExpenseForm(forms.ModelForm):
    long_term = forms.BooleanField(required=False)


    class Meta:
        model = Expense
        fields = ['name', 'amount', 'interest_rate', 'date', 'end_date', 'long_term']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'long_term': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


        def clean(self):
            cleaned_data = super().clean()
            long_term = cleaned_data.get("long_term")
            start_date = cleaned_data.get('date')
            if long_term:
                interest_rate = cleaned_data.get('interest_rate')
                end_date = cleaned_data.get('end_date')
                amount = cleaned_data.get('amount')
                cleaned_data['long_term'] = True     #cleaned_date
            else:
                cleaned_data['end_date'] = None
                cleaned_data['interest_rate'] = None 

            return cleaned_data

