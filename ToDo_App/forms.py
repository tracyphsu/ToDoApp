from django import forms

from .models import *


class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, 
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Task...', 'aria-label': 'Task', 'aria-describedby': 'add-btn' }
        ))

class MealForm(forms.Form):
    meal = forms.CharField(max_length=250, 
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Meal...', 'aria-label': 'Meal', 'aria-describedby': 'add-btn' }
        ))
    day = forms.CharField(max_length=9, 
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Day of the Week...', 'aria-label': 'Day', 'aria-describedby': 'add-btn' }
        ))
    # CHOICES = (
    #     ('1', 'sunday'),
    #     ('2', 'monday'),
    #     ('3', 'tuesday'),
    #     ('4', 'wednesday'),
    #     ('5', 'thursday'),
    #     ('6', 'friday'),
    #     ('7', 'saturday'),
    # )
    # day = forms.ChoiceField(widget=forms.Select, choices=CHOICES)

class BillForm(forms.Form):
    bill = forms.CharField(max_length=250, 
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Bill...', 'aria-label': 'Bill', 'aria-describedby': 'add-btn' }
        ))
    due_date = forms.DateField( 
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Due Date...', 'aria-label': 'Bill', 'aria-describedby': 'add-btn' }
        ))


class GroceryForm(forms.Form):
    item = forms.CharField(max_length=250, 
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Grocery...', 'aria-label': 'Grocery', 'aria-describedby': 'add-btn' }
        ))

class EventForm(forms.Form):
    summary = forms.CharField(max_length=250, 
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Summary...', 'aria-label': 'Summary', 'aria-describedby': 'add-btn' }
        ))
    location = forms.CharField(max_length=250, 
    widget= forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Add Location...', 'aria-label': 'Location', 'aria-describedby': 'add-btn' }
        ))
    description = forms.CharField(max_length=250, 
    widget= forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Add Description...', 'aria-label': 'Description', 'aria-describedby': 'add-btn' }
        ))
    start = forms.DateField( 
    widget= forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Add Start Date...', 'aria-label': 'Start Date', 'aria-describedby': 'add-btn' }
        ))
    end = forms.DateField( 
    widget= forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Add End Date...', 'aria-label': 'End Date', 'aria-describedby': 'add-btn' }
        ))