from django.db import models
from money.contrib.django.models.fields import *
from money.contrib.django.models.managers import *


class Entity(models.Model):
    name = models.CharField(max_length=100)
    price = MoneyField(max_digits=12, decimal_places=3)
    
    objects = MoneyManager()
    
    def __unicode__(self):
        return self.name + " " + str(self.price)
