from django.db import models
from django.contrib.auth.models import User

class loan_data(models.Model):
    created_by = models.ForeignKey(User)
    fname=models.CharField(max_length=30)
    email=models.EmailField()
    currency=models.CharField(max_length=30)
    amount=models.IntegerField()
    interest=models.IntegerField()
    deadline=models.DateField()
    def __unicode__(self):
        return self.fname


class budget(models.Model):
    created_by=models.ForeignKey(User)
    category=models.CharField(max_length=30)
    month=models.CharField(max_length=30)
    year=models.CharField(max_length=30)
    amount=models.IntegerField()
    def __unicode__(self):
        return self.category


class transactions(models.Model):
    created_by=models.ForeignKey(User)
    category=models.CharField(max_length=30)
    amount=models.IntegerField()
    created_date=models.DateField()
    def __unicode__(self):
        return self.category

