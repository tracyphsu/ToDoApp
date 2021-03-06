from __future__ import print_function

from django.contrib.auth.models import User
from apiclient.discovery import build
from httplib2 import Http
import httplib2
import os
from oauth2client import file
import json


from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


import datetime

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

from django.shortcuts import render, redirect 
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task, Grocery, Bill, Meal, Event
from .forms import TaskForm, MealForm, BillForm, GroceryForm, EventForm
from django.contrib import messages
from django.core import serializers
import bcrypt

class CustomLoginView(LoginView):
    template_name= 'ToDo_App/login.html'
    fields= '__all__'
    redirect_authenticated_user= True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name= 'ToDo_App/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user= True
    success_url= reverse_lazy('tasks')

    def form_valid(self, form):
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

@login_required
def tasks(request):
    tasks= Task.objects.filter(user=request.user)
    counts = Task.objects.filter(user=request.user, complete=False)

    form= TaskForm()
    context = {'tasks':tasks, 'form': form, 'counts': counts}
    return render(request, 'ToDo_App/task_list.html', context)

class TaskDetail(LoginRequiredMixin, DetailView):
    model= Task
    context_object_name= 'task'
    template_name= 'ToDo_App/task.html'

@login_required
@require_POST
def taskCreate(request):
    if request.method == "POST":
        form= TaskForm(request.POST)

        if form.is_valid():
            new_task= Task(user=request.user, title=request.POST['title'])
            new_task.save()

    return redirect('/')

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model= Task
    fields= ['title', 'description', 'complete', 'category', 'due_date']
    success_url= reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model= Task
    context_object_name= 'task'
    success_url= reverse_lazy('tasks')    

@login_required
def groceries(request):
    groceries= Grocery.objects.filter(user=request.user)
    counts = Grocery.objects.filter(user=request.user, complete=False)

    form= GroceryForm()
    context = {'groceries':groceries, 'form': form, 'counts': counts}
    return render(request, 'ToDo_App/grocery_list.html', context)

@login_required
@require_POST
def groceryCreate(request):
    form= GroceryForm(request.POST)

    if form.is_valid():
        new_task= Grocery(user=request.user, item=request.POST['item'])
        new_task.save()

    return redirect('/groceries')

class GroceryList(LoginRequiredMixin, ListView):
    model = Grocery
    context_object_name= 'groceries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groceries']= context['groceries'].filter(user=self.request.user)
        context['count']= context['groceries'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input: 
            context['groceries'] = context['groceries'].filter(item__startswith=search_input)

        context['search_input'] = search_input

        return context

class GroceryUpdate(LoginRequiredMixin, UpdateView):
    model= Grocery
    fields= ['item', 'category', 'complete']
    success_url= reverse_lazy('groceries')

class GroceryDelete(LoginRequiredMixin, DeleteView):
    model= Grocery
    context_object_name= 'groceries'
    success_url= reverse_lazy('groceries')

@login_required
def grocery_complete(request, id):
    mark_complete = Grocery.objects.get(id=id)
    mark_complete.complete=True;
    mark_complete.save()
    return redirect('/groceries')

@login_required
def grocery_incomplete(request, id):
    mark_complete = Grocery.objects.get(id=id)
    mark_complete.complete=False;
    mark_complete.save()
    return redirect('/groceries')

@login_required
def delete_grocery(request, id):
    delete_grocery = Grocery.objects.get(id=id)
    delete_grocery.delete()
    return redirect('/groceries')

@login_required
def task_complete(request, id):
    mark_complete = Task.objects.get(id=id)
    mark_complete.complete=True;
    mark_complete.save()
    return redirect('/')

@login_required
def task_incomplete(request, id):
    mark_complete = Task.objects.get(id=id)
    mark_complete.complete=False;
    mark_complete.save()
    return redirect('/')

@login_required
def delete_task(request, id):
    delete_task = Task.objects.get(id=id)
    delete_task.delete()
    return redirect('/')

@login_required
def bills(request):
    bills= Bill.objects.filter(user=request.user)
    counts = Bill.objects.filter(user=request.user, paid=False)

    form= BillForm()
    context = {'bills':bills, 'form': form, 'counts': counts}
    return render(request, 'ToDo_App/bill_list.html', context)

# @login_required
# @require_POST
# def billCreate(request):
#     form= BillForm(request.POST)
#     if form.is_valid():
#         new_bill= Bill(user=request.user, bill=request.POST['bill'], due_date=request.POST['due_date'])
#         new_bill.save()
#     return redirect('/bills')

class BillList(LoginRequiredMixin, ListView):
    model = Bill
    context_object_name= 'bills'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills']= context['bills'].filter(user=self.request.user)
        context['count']= context['bills'].filter(paid=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input: 
            context['bills'] = context['bills'].filter(bill__startswith=search_input)

        context['search_input'] = search_input

        return context

class BillUpdate(LoginRequiredMixin, UpdateView):
    model= Bill
    fields= ['bill', 'category', 'due_date', 'paid']
    success_url= reverse_lazy('bills')

class BillDelete(LoginRequiredMixin, DeleteView):
    model= Bill
    context_object_name= 'bills'
    success_url= reverse_lazy('bills')

@login_required
def bill_paid(request, id):
    mark_paid = Bill.objects.get(id=id)
    mark_paid.paid=True;
    mark_paid.save()
    return redirect('/bills')

@login_required
def bill_notpaid(request, id):
    mark_notpaid = Bill.objects.get(id=id)
    mark_notpaid.paid=False;
    mark_notpaid.save()
    return redirect('/bills')

@login_required
def delete_bill(request, id):
    delete_bill = Bill.objects.get(id=id)
    delete_bill.delete()
    return redirect('/bills')

@login_required
def meals(request):
    meals= Meal.objects.filter(user=request.user)
    counts = Meal.objects.filter(user=request.user, complete=False)
    sunday = Meal.objects.all().filter(user=request.user, day="sunday")
    monday = Meal.objects.all().filter(user=request.user, day="monday")
    tuesday = Meal.objects.all().filter(user=request.user, day="tuesday")
    wednesday = Meal.objects.all().filter(user=request.user, day="wednesday")
    thursday = Meal.objects.all().filter(user=request.user, day="thursday")
    friday = Meal.objects.all().filter(user=request.user, day="friday")
    saturday = Meal.objects.all().filter(user=request.user, day="saturday")

    form= MealForm()
    context = {'meals':meals, 'form': form, 'counts': counts, 'sunday': sunday, 'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday, 'thursday': thursday, 'friday': friday, 'saturday': saturday}
    return render(request, 'ToDo_App/meal_list.html', context)

@login_required
@require_POST
def mealCreate(request):
    form= MealForm(request.POST)

    if form.is_valid():
        new_task= Meal(user=request.user, meal=request.POST['meal'], day=request.POST['day'])
        new_task.save()

    return redirect('/meals')

class MealList(LoginRequiredMixin, ListView):
    model = Meal
    context_object_name= 'meals'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals']= context['meals'].filter(user=self.request.user)
        context['count']= context['meals'].filter(complete=False).count()

        return context

class MealUpdate(LoginRequiredMixin, UpdateView):
    model= Meal
    fields= ['meal', 'day', 'complete']
    success_url= reverse_lazy('meals')

class MealDelete(LoginRequiredMixin, DeleteView):
    model= Meal
    context_object_name= 'meals'
    success_url= reverse_lazy('meals')

@login_required
def delete_meal(request, id):
    delete_meal = Meal.objects.get(id=id)
    delete_meal.delete()
    return redirect('/meals')

@login_required
def meal_complete(request, id):
    mark_complete = Meal.objects.get(id=id)
    mark_complete.complete=True;
    mark_complete.save()
    return redirect('/meals')

@login_required
def meal_incomplete(request, id):
    mark_incomplete = Meal.objects.get(id=id)
    mark_incomplete.complete=False;
    mark_incomplete.save()
    return redirect('/meals')

@login_required
def event_list(request):
        return render(request, 'ToDo_App/event_list.html')

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'credentials.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_event(request):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
                if flags else tools.fun(flow,store)

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = {
        'summary': request.POST['summary'],
        'location': request.POST['location'],
        'description': request.POST['description'],
        'start': {
            'date': request.POST['start_date'],
        },
        'end': {
            'date': request.POST['end_date'],
        },
    }
    # json_event = json.dumps(event)
    event = service.events().insert(calendarId='bb3c6jev76jlkm8n43b1knkhco@group.calendar.google.com', body=event).execute()

    form= EventForm(request.POST)

    if form.is_valid():
        new_event= Event(summary=request.POST['summary'], location=request.POST['location'], description=request.POST['description'], start=request.POST['start_date'], end=request.POST['end_date'])
        new_event.save()

    return redirect('/ToDo_App/event-list')

@login_required
@require_POST
def billCreate(request):
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
                if flags else tools.fun(flow,store)

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = {
        'summary': request.POST['bill'] + " Bill Due",
        'start': {
            'date': request.POST['due_date'],
        },
        'end': {
            'date': request.POST['due_date'],
        },
    }
    # json_event = json.dumps(event)
    event = service.events().insert(calendarId='bb3c6jev76jlkm8n43b1knkhco@group.calendar.google.com', body=event).execute()
    form= BillForm(request.POST)

    if form.is_valid():
        new_bill= Bill(user=request.user, bill=request.POST['bill'], due_date=request.POST['due_date'])
        new_bill.save()

    return redirect('/bills')

class EventCreate(LoginRequiredMixin, CreateView):
    model= Event
    fields = ['summary', 'location', 'description', 'start_date', 'end_date']
    success_url= reverse_lazy('/ToDo_App/event-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate, self).form_valid(form)
