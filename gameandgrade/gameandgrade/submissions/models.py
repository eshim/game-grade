from django.db import models
from django.contrib.auth.models import User
import datetime

class UserID(models.Model):
    user = models.ForeignKey(User)
    def __unicode__(self):
        return str(self.user.username)
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    descrip = models.TextField('Description')
    xpVal = models.IntegerField('Maximum Experience')
    openTime = models.DateTimeField('Start Time')    
    closeTime = models.DateTimeField('End Time')   
    def isOpen(self):
        return (datetime.datetime.now() >= self.openTime) and (datetime.datetime.now() <= self.closeTime)
    isOpen.admin_order_field = 'openTime'
    isOpen.boolean = True
    isOpen.short_description = 'Currently Open?'
    def __unicode__(self):
        return self.title
    
class Exercise(models.Model):
    task = models.ForeignKey(Task)
    title = models.CharField(max_length=200)
    descrip = models.TextField('Description')
    xpVal = models.IntegerField('Maximum Experience')
    tags = models.CharField(max_length=100)
    def __unicode__(self):
        return self.title

class Upload(models.Model):
    title = models.CharField(max_length=50)
    fileName = models.CharField(max_length=50, blank=True, null=True)
    fileUpload = models.FileField(upload_to='file_uploads')
    userID = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    uploadTime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title