from django.db import models
from django.contrib.auth.models import User

from oauth2client.django_orm import FlowField,CredentialsField
# Create your models here.

class Oauth(models.Model):
	user = models.ForeignKey(User, primary_key=True)
	flow = FlowField()
	credential = CredentialsField()

	def __unicode__(self):
	    return '['+str(self.pk)+'] '+self.user.username