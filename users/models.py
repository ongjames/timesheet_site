from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# for optional things,eg
# comments, profile pic etc
class UserProfile(models.Model):
	user = models.ForeignKey(User,primary_key=True)
	comments = models.CharField(max_length=128,blank=True)

	def __unicode__(self):
	    return '['+str(self.pk)+'] '+self.user.username

class PrivateMessage(models.Model):
	to_user = models.ForeignKey(User,related_name='to_user',related_query_name='to_user')
	from_user = models.ForeignKey(User,related_name='from_user',related_query_name='from_user')
	message_time = models.DateTimeField()
	message = models.CharField(max_length=128)

	def __unicode__(self):
	    return '['+str(self.pk)+'] (To '+self.to_user.username+') (From '+self.from_user.username+')'