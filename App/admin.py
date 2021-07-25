from django.contrib import admin
from .models import BlogModel, Profile, email_verification

# Register your models here.

admin.site.register(BlogModel)
admin.site.register(Profile)
admin.site.register(email_verification)