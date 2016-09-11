from django.db import models

# Create your models here.

class Users(models.Model):
	user_name = models.CharField(max_length=128, unique=True)
	password = models.CharField(max_length=128)
	title = models.CharField(max_length=128)
	content = models.CharField(max_length=128)

	def __unicode__(self):
		return self.user_name