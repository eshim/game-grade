from django.db import models

class User(models.Model):
    first = models.CharField(max_length=50)    
    last = models.CharField(max_length=50)
    createTime = models.DateTimeField('When Created')
    email = models.CharField(max_length=50)
    twitter = models.CharField(max_length=50)
    website = models.CharField(max_length=100)
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    descrip = models.TextField('Description')
    xpVal = models.IntegerField('Maximum Experience')
    openTime = models.DateTimeField(auto_now=True)    
    closeTime = models.DateTimeField(auto_now=True)
    
class Submission(models.Model):
    userID = models.ForeignKey(User)
    taskID = models.ForeignKey(Task)
    submitTime = models.DateTimeField(auto_now=True)
#    ptsGiv = models.FloatField() --Commented because it gave errors. Will figure out later.

class Upload(models.Model):
    title = models.CharField(max_length=50)
    fileUpload = models.FileField(upload_to = 'file_uploads')