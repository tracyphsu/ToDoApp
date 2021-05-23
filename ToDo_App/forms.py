from django import forms

from .models import *


class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, 
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Add Task...', 'aria-label': 'Task', 'aria-describedby': 'add-btn' }
        ))