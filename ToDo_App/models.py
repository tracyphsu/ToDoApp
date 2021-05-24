from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class TaskManager(models.Manager):
    def task_validator(self, form):
        errors = {}

        if len(form['title']) < 3:
            errors['title'] = "A title name must be provided and consist of at least 3 characters!"
        if len(form['description']) < 2:
            errors['description'] = "A description must be provided and consist of at least 2 characters!"
        if datetime.strptime(form['due_date'], '%Y-%m-%d') > datetime.now():
            errors["due_date"] = "Due date should be in the past"     
        return errors

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    complete = models.BooleanField(default=False)
    category = models.CharField(max_length=50)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

class GroceryManager(models.Manager):
    def grocery_validator(self, form):
        errors = {}

        if len(form['item']) < 3:
            errors['item'] = "An item name must be provided and consist of at least 3 characters!"
        return errors

class Grocery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item= models.CharField(max_length=100)
    complete= models.BooleanField(default=False)
    category= models.CharField(max_length= 50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item

    class Meta:
        ordering = ['complete']

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bill= models.CharField(max_length= 100)
    paid= models.BooleanField(default=False)
    category= models.CharField(max_length=50)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bill

    class Meta:
        ordering = ['paid']

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    meal= models.CharField(max_length= 250)
    complete=models.BooleanField(default=False)
    day=models.CharField(max_length=9, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meal

    class Meta:
        ordering= ['complete']

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    summary= models.CharField(max_length= 250, null=True, blank=True)
    location= models.CharField(max_length= 250, null=True, blank=True)
    description= models.CharField(max_length= 250, null=True, blank=True)
    date= models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.summary

    class Meta:
        ordering= ['date']
