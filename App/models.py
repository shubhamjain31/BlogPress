from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField

from .helpers import *

# Create your models here.

class Profile(models.Model):
    user 			= models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified 	= models.BooleanField(default=False)
    token 			= models.CharField(max_length=100)
    image           = models.ImageField(upload_to='media/images/', default='media/images/profile.png', blank=True)
    about           = models.CharField(max_length=200, blank=True , null=True)
    mobile 			= models.CharField(max_length=15)
    date_created    = models.DateTimeField(auto_now_add=True)
    ip_address      = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)

class email_verification(models.Model):

    user                        = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_link           = models.CharField(max_length=200)
    created_date                = models.DateTimeField(auto_now_add=True)
    ip_address                  = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user)
    

class BlogModel(models.Model):
	user 			= models.ForeignKey(User, blank=True , null=True , on_delete=models.CASCADE)
	title 			= models.CharField(max_length=1000)
	content 		= FroalaField()
	slug 			= models.SlugField(max_length=1000 , null=True , blank=True)
	image 			= models.ImageField(upload_to='blog')
	created_at 		= models.DateTimeField(auto_now_add=True)
	upload_to 		= models.DateTimeField(auto_now=True)
	browser 		= models.CharField(max_length=200)
	ip_address		= models.CharField(max_length=100)

	def __str__(self):
	    return self.title

	def save(self , *args, **kwargs): 
	    self.slug = generate_slug(self.title)
	    super(BlogModel, self).save(*args, **kwargs)