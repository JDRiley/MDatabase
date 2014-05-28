from django.db import models

class Dot11Radio_Entry(models.Model):
    M_Controller_name = models.CharField(max_length=255)
    M_date = models.DateTimeField('Date')


