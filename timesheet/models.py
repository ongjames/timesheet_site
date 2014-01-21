from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile

# Create your models here.


class Time(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField()
    hours = models.IntegerField()
    comments = models.CharField(max_length=128,blank=True)
    user = models.ForeignKey(User)

    class Meta:
    	ordering = ['date']

    def __unicode__(self):
        return '['+str(self.pk)+'] ('+str(self.date)+') '+self.title