from django.db                  import models
from django.contrib.auth.models import User
from datetime                   import datetime

import pytz

class UserID(models.Model):
    """
    Creates a user object that we can manipulate more so than the Django user
    """
    
    user = models.ForeignKey(User, verbose_name='Username')
    
    def __unicode__(self):
        return str(self.user.username)


class Task(models.Model):
    """
    Allows the creation of tasks, which are essentially a full assignment
    """
    
    title = models.CharField(default = ' ' ,max_length=200)
    fileName = models.CharField('File Name', max_length=50)
    descrip = models.TextField('Description')
    xpVal = models.IntegerField('Maximum Experience')
    openTime = models.DateTimeField('Start Time')    
    closeTime = models.DateTimeField('End Time')   
    
    def isOpen(self):
        return (datetime.now(pytz.utc) >= self.openTime) and (datetime.now(pytz.utc) <= self.closeTime)
    
    isOpen.admin_order_field = 'openTime'
    isOpen.boolean = True
    isOpen.short_description = 'Currently Open?'
        
    def __unicode__(self):
        return self.title
    

class Exercise(models.Model):
    """
    Allows the creation of exercises, which are portions of skills to be utilized in tasks. 
    Not implemented as of this update.
    """
    
    task = models.ForeignKey(Task)
    title = models.CharField(max_length=200)
    descrip = models.TextField('Description')
    xpVal = models.IntegerField('Maximum Experience')
    tags = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.title


class Upload(models.Model):
    """
    For file uploads. Allows custom titling (which will soon be taken away), auto assignment of upload time, 
    and relationship to the current user's ID and the task it is being submitted to, so that submissions are 
    viewed organized by user and task 
    """
    
    id = models.AutoField(primary_key=True)
    fileUpload = models.FileField(upload_to='file_uploads')
    userID = models.ForeignKey(User, verbose_name='Username')
    task = models.ForeignKey(Task)
    uploadTime = models.DateTimeField('Uploaded On', auto_now_add=True)
    mostRecent = models.BooleanField('Most Recent', default=True)
    uploadURL = models.URLField('URL', default=" ")        
    
    
    def __unicode__(self):
        return self.id 
    
    
class UnitTest(models.Model):
    """
    Allows the instructor to upload a series of evaluators for testing students' code to make sure specific 
    requirements are met.
    """
    
    name = models.CharField('Evaluator Name', max_length=50)
    file = models.FileField(upload_to='instructor_files/evals')
    tasks = models.ManyToManyField(Task, verbose_name='Associated Tasks')