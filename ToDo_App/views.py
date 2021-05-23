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

# def create_event(request):
#     calendar = {
#     'summary': 'calendarSummary',
#     'timeZone': 'America/Los_Angeles'
# }

#     created_calendar = service.calendars().insert(body=calendar).execute()

# def google_calendar_connection():
#     """
#     This method used for connect with google calendar api.
#     """
    
#     flags = tools.argparser.parse_args([])
#     FLOW = OAuth2WebServerFlow(
#         scope='https://www.googleapis.com/auth/calendar',
#         credentials = ServiceAccountCredentials.from_json_keyfile_name(filename="credentials.json", scopes=SCOPES,

#         )
#     storage = Storage('calendar.dat')
#     credentials = storage.get()
#     if credentials is None or credentials.invalid == True:
#         credentials = tools.run_flow(FLOW, storage, flags)
    
#     # Create an httplib2.Http object to handle our HTTP requests and authorize it
#     # with our good Credentials.
#     http = httplib2.Http()
#     http = credentials.authorize(http)
#     service = discovery.build('calendar', 'v3', http=http)
    
#     return service

# def event_form(self, form):
#     """
#     This method used for add event in google calendar.
#     """
    
#     service = self.google_calendar_connection()
    
#     event = {
#         'summary': "new",
#         'location': "london",
#         'description': "anything",
#         'start': {
#         'date': "2015-09-02",
#         },
#         'end': {
#         'date': "2015-09-02",
#         },
                
#     }
    
#     event = service.events().insert(calendarId='primary', body=event).execute()
    
#     return CreateView.form_valid(self, form) 