from django.db import models
from django.utils import timezone

class Books(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    author = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)


class Users(models.Model):
    name = models.CharField(max_length=255)
    outstanding_amount = models.FloatField()

class Transaction(models.Model):
    books = models.ForeignKey("Books",on_delete=models.CASCADE)
    users = models.ForeignKey("Users",on_delete=models.CASCADE)
    taken_on = models.DateTimeField(auto_now=True)
    return_on = models.DateTimeField()
