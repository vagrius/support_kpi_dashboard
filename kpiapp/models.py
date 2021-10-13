from django.db import models


# class Company(models.Model):
#     url = models.CharField(max_length=64)
#     name = models.CharField(max_length=128)


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
    url_uid = models.CharField(max_length=128, default='0')


class Update(models.Model):
    date_time = models.DateTimeField()
    first_link = models.CharField(max_length=64, default='0')
