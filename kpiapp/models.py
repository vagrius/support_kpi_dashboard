from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# class Specialist(models.Model):
#     name = models.CharField(max_length=64)
#
#
# class Company(models.Model):
#     uid = models.CharField(max_length=64)
#     name = models.CharField(max_length=128)
#     request_last_date = models.DateField()


class Request(models.Model):
    date_time = models.DateTimeField()
    company = models.CharField(max_length=128)
    customer_name = models.CharField(max_length=128)
    request_text = models.TextField()
    reactions = models.CharField(max_length=256)
    decision_time = models.FloatField()
    specialist = models.CharField(max_length=128)
    dec_in_time = models.PositiveIntegerField()
    reactions_count = models.PositiveIntegerField()
    reactions_in_time_count = models.PositiveIntegerField()
    reactions_average = models.FloatField()
