from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from exp_tracker import models
from .models import Account, Expense
from .forms import ExpenseForm, CustomUserCreationForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count, F
import plotly.express as px
from plotly.graph_objs import *


# Create your views here.

def home(request):
    return render(request, 'home/home.html')


from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

class CustomUserCreationForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default help text
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['toast_message'] = {
                'message': 'Registration successful! Please log in with your credentials.',
                'type': 'success'
            }
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['toast_message'] = {
                    'message': f'Welcome back, {username}!',
                    'type': 'success'
                }
                return redirect('expenses')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
@require_http_methods(['GET', 'POST'])
def logout_view(request):
    logout(request)
    request.session['toast_message'] = {
        'type': 'success',
        'message': 'You have been logged out successfully.'
    }
    return redirect('home')


def generate_graph(data):
    fig = px.bar(data, x='months', y='expenses', title='Monthly Expenses')
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color = 'rgba(0,0,0,1)'
    )
    fig.update_traces(marker_color='#008c41')

    graph_json = fig.to_json()
    return graph_json


class ExpenseListView(FormView):
    template_name = 'exp_tracker/expenses_list.html'
    form_class = ExpenseForm
    success_url = '/'

    def form_valid(self, form):
        account, _ = Account.objects.get_or_create(user=self.request.user)

        expense = Expense(
            name = form.cleaned_data['name'],
            amount = form.cleaned_data['amount'],
            interest_rate = form.cleaned_data['interest_rate'],
            date = form.cleaned_data['date'],
            end_date = form.cleaned_data['end_date'],
            long_term = form.cleaned_data['long_term'],
            user = self.request.user
        )
        expense.save()
        account.expense_list.add(expense)
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = Account.objects.filter(user=user)

        expense_data_graph = {}
        expense_data = {}

        for account in accounts:
            expenses = account.expense_list.all()
            for expense in expenses:
                if expense.long_term and expense.monthly_expenses:
                    current_date = expense.date
                    while current_date <= expense.end_date:
                        year_month = current_date.strftime('%Y-%m')
                        if year_month not in expense_data_graph:
                            expense_data_graph[year_month] = []

                        expense_data_graph[year_month].append({
                            'name': expense.name,
                            'amount': expense.monthly_expenses,
                            'date': expense.date,
                            'end_date': expense.end_date,
                        })

                        current_date = current_date + relativedelta(months=1)
                else:
                    year_month = expense.date.strftime('%Y-%m')
                    if year_month not in expense_data_graph:
                        expense_data_graph[year_month] = []

                        expense_data_graph[year_month].append({
                            'name': expense.name,
                            'amount': expense.amount,
                            'date': expense.date,
                        })

        for account in accounts:
            expenses = account.expense_list.all()
            for expense in expenses:
                if expense.long_term and expense.monthly_expenses:
                    current_date = expense.date
                    year_month = current_date.strftime('%Y-%m')
                    if year_month not in expense_data:
                        expense_data[year_month] = []

                    expense_data[year_month].append({
                        'name': expense.name,
                        'amount': expense.amount,
                        'date': current.date,
                        'end_date': expense.end_date,
                        'long_term': expense.long_term,
                    })

                        # Move to the next month
                    current_date = current_date + relativedelta(months=1)
                else:
                    year_month = expense.date.strftime('%Y-%m')
                    if year_month not in expense_data:
                        expense_data[year_month] = []

                    expense_data[year_month].append({
                        'name': expense.name,
                        'amount': expense.amount,
                        'date': expense.date,
                    })

        aggregated_data = [{ 'year_month': key, 'expenses': sum(item['amount'] for item in value)} for key, value in expense_data_graph.items()]

        context['expense_data'] = expense_data
        context['aggregated_data'] = aggregated_data

        graph_data = {
            'months': [item['year_month'] for item in aggregated_data],
            'expenses': [item['expenses'] for item in aggregated_data],
        }

        graph_data['chart'] = generate_graph(graph_data)
        context['graph_data'] = mark_safe(graph_data['chart'])

        return context

        