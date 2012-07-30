from gameandgrade.submissions.models import Task, Upload, UserID, UnitTest
from gameandgrade.submissions.upload import UploadForm
from gameandgrade                    import parser

from django.contrib.auth.decorators  import login_required
from django.contrib.auth             import authenticate, logout
from django.db.models.signals        import post_save
from django.dispatch                 import receiver

from django.core.files.storage       import default_storage
from django.shortcuts                import render_to_response
from django.http                     import HttpResponseRedirect
from django.template                 import RequestContext
from django.core                     import files

from django.db                       import models
from django.core.files.base          import ContentFile 

from django.contrib.auth.models      import User
from gameandgrade                    import settings
from datetime                        import datetime

import subprocess
import shlex
import os

    
def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    
    logout(request)
    return HttpResponseRedirect('/tasks')  # This will need to change to '/' once we create a home page.


@login_required(login_url='/login/')  # This is required until the concept of the Guest view is created so that code won't error.
def tasks(request):
    """
    Displays tasks organized by start and end time
    """
    
    filtSubs = Upload.objects.filter(
            userID=request.user).order_by('-uploadTime') # This gets all upload objects a particular user submitted
    allTasks = Task.objects.all().order_by('-openTime')
    openTasks=[]
    closedTasks=[]
    
    for x in allTasks:
        if datetime.now() < x.openTime:  # This is so that tasks that are created before starting time are viewable until then.
            pass
        elif (datetime.now() >= x.openTime and 
              datetime.now() <= x.closeTime):  # Or, in other words, if it's during the lifetime of the task.
            openTasks.append(x)
        else:  # If it's after the task has closed, add it to the closedTasks list
            closedTasks.append(x)

    return render_to_response(
        'GameAndGrade_Base_StudentTasks.html',
        {'openTasks': openTasks, 'closedTasks': closedTasks, 'filtSubs': filtSubs},
        context_instance=RequestContext(request))


@login_required(login_url='/login/')  # This is required until the concept of the Guest view is created so that code won't error.
def uploadFile(request):
    """
    Uploads a submissions file to be viewed on the site
    """
    
    # The following function will set a mostRecent flag to true to determine a user's most recent submission for each task.
    def setMostRecent(upload):
        sameSubType = Upload.objects.filter(userID=upload.userID, task=upload.task)
        
        for sub in sameSubType:
            sub.mostRecent = False
            sub.save()
        
        upload.mostRecent = True
        upload.save()
        
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            myFile = request.FILES['fileUpload']
            upload_instance = form.save(commit=False)  # Saves the form but don't commit it since some fields are still empty.
            upload_instance.userID = request.user  # Saves the current user's id to ForeignKey to allow sorting in Tasks view.
            upload_instance.task = Task.objects.get(
                    pk=request.POST['taskID'])  # Save the current task's ID to allow sorting in Tasks view
            saveLocation = str(upload_instance.userID)
            
            try:  # Try to make a directory with user's name if not created for file uploads.
                os.makedirs(os.path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation))
            except:
                pass
            try:  # Try to make a directory with user's name if not created for PyLint output.
                os.makedirs(os.path.join(settings.MEDIA_ROOT,'evaluated_code/pylint', saveLocation))
            except:
                pass
            try:
                os.makedirs(os.path.join(settings.MEDIA_ROOT,'evaluated_code/unit_tests', saveLocation))
            except:
                pass
            
            fileName = upload_instance.title  # This is what the uploaded file's name will be.

            default_storage.save(os.path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation, fileName), myFile)  # Save to disc          
            upload_instance.fileUpload = os.path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation, fileName)
            
            upload_instance.save()  # post_save method is called to generate PyLint output from the uploaded file.
            
            setMostRecent(upload_instance)
            
            return HttpResponseRedirect('/tasks/')
        else: 
            return HttpResponseRedirect('/tasks/')  # If not valid, reloads task page - eventually may be preventable.
    else:
        form = Upload()
    
    return render_to_response('GameAndGrade_Base_StudentTasks.html', {'form': form})


def uploadCode(request):
   """ 
   Uploads the pasted code as a submissions file to be viewed on the site
   """
   if request.method == 'POST':
       form = UploadCodeForm(dict(request.POST)) # Request File, but not a file/ That's why there's n

       if form.is_valid():
           fileName = request.POST['title'] # This is what the uploaded file's name will be.
           code = request.POST['code'] #This requests the code input
           taskID = request.POST['taskID'] #This requests the taskID
           task = Task.objects.get(pk=taskID)  # Save the current task's ID to allow sorting in Tasks
           user = request.user  # Saves the current user's id to ForeignKey to allow sorting in Tasks
           userID = str(user)  #Converts the user's ID to string type for reference
           
           try:  # Try to make a directory with user's name if not created for file uploads.
               makedirs(path.join(settings.MEDIA_ROOT,'file_uploads', userID))
           except:
               pass
           try:  # Try to make a directory with user's name if not created for PyLint output.
               makedirs(path.join(settings.MEDIA_ROOT,'evaluated_code', userID))
           except:
               pass
           
           upload_instance = Upload(title=fileName, userID=user, task=task) #Creating the upload instance
           default_storage.save(path.join(settings.MEDIA_ROOT,'file_uploads', userID, fileName),ContentFile(code))
           upload_instance.fileUpload = path.join(settings.MEDIA_ROOT, 'file_uploads', userID, fileName)
           upload_instance.save()  # post_save method is called to generate PyLint output from the up

           return HttpResponseRedirect(path.join("../subs",str(upload_instance.id)))
       
       
def newSub(request):
   """
   Sends you to a new blank submission form
   """

   if request.method == 'POST':
       form = UploadForm(request.POST)

       if form.is_valid():
           taskID = request.POST['taskID']

       return render_to_response('ViewSubmissions.html',
                             {'currSub': " ", 'evalSub': None, 'submission': None, 'taskID': request},
                             context_instance=RequestContext(request))


@receiver(post_save, sender=Upload)  # When an Upload object is saved, also do the following function
def evaluate(sender, **kwargs):
    """
    Will generate a PyLint output file that evaluates an uploaded file and a Unit Test file that checks code against requirements.    
    """
    
    evals = UnitTest.objects.filter(tasks=kwargs['instance'].task)
    inPath = str(kwargs['instance'].fileUpload)  # The path to the user's uploaded code
    outPathLint = inPath.replace('file_uploads','evaluated_code/pylint')  # The path to the generated PyLint output
    
    # The following if statement is to ensure that the code isn't repeated more than once, despite the save method being called
    # multiple times.
    if not os.path.exists(outPathLint):  
        outPathTest = inPath.replace('file_uploads','evaluated_code/unit_tests')  # The path to the generated PyLint output
        inPath = inPath.replace(' ','\ ')  # This prevents spaces in the inpath from becoming individual shell commands
        cmdLine = 'pylint --reports=n --include-ids=y --disable=F,I,R,W ' + inPath  # Builds the command to be run by the shell 
        cmds = shlex.split(cmdLine)  # This makes the commands above readable to the shell.
        p = subprocess.Popen(cmds,stdout=open(outPathLint,'w'))  # This executes the command created and saves output
        stdout,stderr = p.communicate()  # Sends output to stdout to be saved.
        
        # The following code will run a series of unit tet evaluators that the instructor will have uploaded for the task.       
        for test in evals:
            evalPath = test.file.path
            evalPath = evalPath.replace(' ', '\ ')
            cmdLine = 'python %s' % (evalPath)
            cmds = shlex.split(cmdLine)
            p = subprocess.Popen(cmds, stderr=subprocess.STDOUT, stdout=open(outPathTest,'a'))
            stdout,stderr = p.communicate()
            

@login_required(login_url='/login/')  # This is required until the concept of the Guest view is created so that code won't err.
def viewSub(request, subID):
    """
    Allows you to view a partcular submission's code and the problems PyLint has found with the code.
    """
    
    s = Upload.objects.get(pk=subID)  # Get the submission that was selected.
    currUser = request.user
    codePath = s.fileUpload.path
    evalCodePath = codePath.replace(
            "file_uploads","evaluated_code/pylint")  # This works since the only difference in paths are this.
    
    with open(codePath, mode='r') as f:
        subString = f.read()    
    
    e = parser.readable_output(evalCodePath)  # Sends path to PyLint file to parser file to make user output user friendly.
    e = e.replace('\n', '<br>')  # Replaces all newline characters with a break tag for formatting -- TO BE CHANGED LATER?
    
    return render_to_response('GameAndGrade_Base_StudentTasks_Submissions_SubmissionCode.html', 
                              {'currSub': subString, 'evalSub': e, 'subs': s}, context_instance=RequestContext(request))