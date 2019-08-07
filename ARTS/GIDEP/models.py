# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import uuid, os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.http import HttpResponse, Http404
from django.template.defaultfilters import slugify
#from django.contrib.auth.models import AbstractUser

# Create your models here.

class Alert(models.Model):
    
    # Information
    classification = models.CharField(max_length=50, unique=True, null=True)
    title = models.CharField(max_length=200, unique=True, null=True)
    link = models.CharField(max_length=200)
    due_date = models.DateField(blank=True, null=True)
    message = models.TextField()
    disclaimer = models.TextField()

# Admin-Editable Dropdowns for Alert Type and Subclass
# https://stackoverflow.com/questions/36690444/customize-dropdown-list-from-django-admin-panel

class AlertType(models.Model):
    type_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.type_name
    
class Subclass(models.Model):
    type_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.type_name

# Built-In Restrictions   
# https://stackoverflow.com/questions/31130706/dropdown-in-django-model

RESTRICTION_CHOICES = (
        ('default', 'Default'),
        ('limited', 'Limited'),
        ('none','None'),
)


class Document(models.Model):
    
    # ARTS Document Information
    arts_ID = models.CharField(max_length=12, default=get_random_string(4).lower() + str(uuid.uuid4())[:8], editable=False) # https://stackoverflow.com/questions/45620977/how-to-create-short-uuid-with-django
    arts_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    arts_date = models.DateTimeField(default=timezone.now, editable=False)
    
    # Classifications
    arts_type = models.ForeignKey('AlertType', null=True)
    arts_subclass = models.ForeignKey('Subclass', null=True)
    distribution_restrictions = models.CharField(max_length=7, choices=RESTRICTION_CHOICES, default='default')
    
    # Root Document Information
    document_number = models.CharField(max_length=200, primary_key=True)
    alternate_tracking_number = models.CharField(max_length=200, unique=True, null=True)
    document_date = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    attachment = models.FileField(upload_to='Uploads')
    
    
    def publish(self, *args, **kwargs):  
        self.document_date = timezone.now()
        super(Document, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('document_detail', (), 
                {
                    '_id' :self.arts_ID,
                })
        
#    def download(request, path):
#        file_path = os.path.join(settings.MEDIA_ROOT, path)
#        if os.path.exists(file_path):
#            with open(file_path, 'rb') as fh:
#                response = HttpResponse(fh.read())
#                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#                return response
#        raise Http404
        
    def __str__(self):
        return self.document_number

# User Models
# https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html

#class User(AbstractUser):
    # Two classes, one can view and comment, the other can add documents and
    # edit choices internally.
#    is_gidep = models.BooleanField(default=False)
#    is_quality = models.BooleanField(default=False)
#    is_commenter = models.BooleanField(default=False)
#    is_poster = models.BooleanField(default=False)
    
#class Account(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#    program = WILL WANT TO ADD APPLICABLE PROGRAM HERE
#    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
#    interests = models.ManyToManyField(Subject, related_name='interested_students')