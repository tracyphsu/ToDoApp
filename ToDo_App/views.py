from __future__ import print_function
import httplib2
import os
from oauth2client import file

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
from .models import Task, Grocery, Bill, Meal 
from .forms import TaskForm
from django.contrib import messages
import bcrypt

# from googleapiclient.discovery import build
# from httplib2 import Http
# from oauth2client import file, client, tools
# from datetime import datetime


# SCOPES = "https://www.googleapis.com/auth/calendar"
# store = file.Storage('token.json')
# creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
#     creds = tools.run_flow(flow, store)
#     service = build('calendar', 'v3', http=creds.authorize(Http()))
# import datetime
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

# from datetime import timedelta

# import pytz

# SCOPES = ["https://www.googleapis.com/auth/calendar"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     filename="credentials.json", scopes=SCOPES
# )


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


def tasks(request):
    tasks= Task.objects.all()
    count = Task.objects.filter().count()

    form= TaskForm()
    context = {'tasks':tasks, 'form': form }
    return render(request, 'ToDo_App/task_list.html', context)

class TaskDetail(LoginRequiredMixin, DetailView):
    model= Task
    context_object_name= 'task'
    template_name= 'ToDo_App/task.html'

@require_POST
def taskCreate(request):
    form= TaskForm(request.POST)

    if form.is_valid():
        new_task= Task(title=request.POST['title'])
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

class GroceryCreate(LoginRequiredMixin, CreateView):
    model= Grocery
    fields = ['item', 'category', 'complete']
    success_url= reverse_lazy('grocery-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GroceryCreate, self).form_valid(form)

class GroceryUpdate(LoginRequiredMixin, UpdateView):
    model= Grocery
    fields= ['item', 'category', 'complete']
    success_url= reverse_lazy('grocery-list')

class GroceryDelete(LoginRequiredMixin, DeleteView):
    model= Grocery
    context_object_name= 'groceries'
    success_url= reverse_lazy('grocery-list')

def grocery_complete(request, id):
    mark_complete = Grocery.objects.get(id=id)
    mark_complete.complete=True;
    mark_complete.save()
    return redirect('/grocery-list')

def grocery_incomplete(request, id):
    mark_complete = Grocery.objects.get(id=id)
    mark_complete.complete=False;
    mark_complete.save()
    return redirect('/grocery-list')

def task_complete(request, id):
    mark_complete = Task.objects.get(id=id)
    mark_complete.complete=True;
    mark_complete.save()
    return redirect('/')

def task_incomplete(request, id):
    mark_complete = Task.objects.get(id=id)
    mark_complete.complete=False;
    mark_complete.save()
    return redirect('/')

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

class BillCreate(LoginRequiredMixin, CreateView):
    model= Bill
    fields = ['bill', 'category', 'due_date', 'paid']
    success_url= reverse_lazy('bill-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BillCreate, self).form_valid(form)

class BillUpdate(LoginRequiredMixin, UpdateView):
    model= Bill
    fields= ['bill', 'category', 'due_date', 'paid']
    success_url= reverse_lazy('bill-list')

class BillDelete(LoginRequiredMixin, DeleteView):
    model= Bill
    context_object_name= 'bills'
    success_url= reverse_lazy('bill-list')

def bill_paid(request, id):
    mark_paid = Bill.objects.get(id=id)
    mark_paid.paid=True;
    mark_paid.save()
    return redirect('/bill-list')

def bill_notpaid(request, id):
    mark_notpaid = Bill.objects.get(id=id)
    mark_notpaid.paid=False;
    mark_notpaid.save()
    return redirect('/bill-list')

class MealList(LoginRequiredMixin, ListView):
    model = Meal
    context_object_name= 'meals'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals']= context['meals'].filter(user=self.request.user)
        context['count']= context['meals'].filter(complete=False).count()

        return context

class MealCreate(LoginRequiredMixin, CreateView):
    model= Meal
    fields = ['meal', 'complete']
    success_url= reverse_lazy('meal-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MealCreate, self).form_valid(form)

class MealUpdate(LoginRequiredMixin, UpdateView):
    model= Meal
    fields= ['meal', 'complete']
    success_url= reverse_lazy('meal-list')

class MealDelete(LoginRequiredMixin, DeleteView):
    model= Meal
    context_object_name= 'meals'
    success_url= reverse_lazy('meal-list')

def meal_complete(request, id):
    mark_complete = Meal.objects.get(id=id)
    mark_complete.complete=True;
    mark_complete.save()
    return redirect('/meal-list')

def meal_incomplete(request, id):
    mark_incomplete = Meal.objects.get(id=id)
    mark_incomplete.complete=False;
    mark_incomplete.save()
    return redirect('/meal-list')


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
    credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')

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
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/google-apps/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    if request.method == "POST":
        
        event = Event.objects.create(
            summary=request.POST['summary'],
            location=request.POST['location'],
            description=request.POST['description'],
            date=request.POST['date'],
        )
        event = service.events().insert(calendarId='primary', body=event).execute()
    return redirect('ToDo_App/event-list')

class EventCreate(LoginRequiredMixin, CreateView):
    model= Event
    fields = ['summary', 'location', 'description', 'date']
    success_url= reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate, self).form_valid(form)