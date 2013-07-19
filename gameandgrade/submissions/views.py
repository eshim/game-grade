from submissions.models import Task, Upload, UserID, UnitTest
from submissions.upload import UploadForm
import gameAndGradeParser
import unitTestParser

from django.contrib.auth.decorators  import login_required
from django.contrib.auth             import authenticate, logout
from django.db.models.signals        import post_save
from django.dispatch                 import receiver

from django.core.files.storage       import default_storage
from django.shortcuts                import render_to_response
from django.http                     import HttpResponse, HttpResponseRedirect
from django.template                 import RequestContext
from django.core                     import files

from django.db                       import models
from django.core.files.base          import ContentFile 

from django.contrib.auth.models      import User
import settings
from datetime                        import datetime

import subprocess
import shlex
import shutil #-------for unit testing
import os

import pytz

def dtToStr(dateTimeObj): 
    """
    Helper function that casts a datetime object to a string.
    """

    return dateTimeObj.strftime(settings.DATEREP)


def dtFromStr(dateTimeStr): 
    """
    Helper function that casts a string in a datetime format to a datetime object.
    """
    
    return datetime.strptime(dateTimeStr, settings.DATEREP)


def uploadTimeFromFileName(fileNameStr): 
    """
    Returns the datetime object at the time the file was uploaded.
    """
    
    extractedDate = fileNameStr.split('.')[0]
    extractedDate = extractedDate[-19:] #Takes the last 19 characters (all of the time/date)
    return dtFromStr(extractedDate) 
    
    
def uploadFileName(userName, taskName, dateTimeStr): 
    """
    Returns string that will be the filename.
    Format is: <user name>_<task name>_<YYYY_MM_DD_HH_MM_SS> according to settings.DATEREP
    """
    
    taskName = str(taskName).replace(' ', '_')
    newFileName = userName + '_' + str(taskName) + '_' + dtToStr(dateTimeStr)
    
    return newFileName


def checkEmpty(infile):
    """
    Helper function that checks if file is empty of content. Returns True if empty.
    """
    
    fin = open(infile)
    content = ''
    
    for n in fin:
        content += n
    
    fin.close()
    
    if content.strip() == '': #remove whitespace/tabs/newlines
        return True
    else:
        return False
    

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    
    logout(request)
    return HttpResponseRedirect('/tasks')  # This will need to change to '/' once we create a home page.


@login_required(login_url='/login/')  # This is required until the concept of the Guest view is created so that code won't error.
def viewTasks(request):
    """
    Displays tasks organized by start and end time
    """
    
    filtSubs = Upload.objects.filter(
            userID=request.user).order_by('-uploadTime') # This gets all upload objects a particular user submitted
    allTasks = Task.objects.all().order_by('-openTime')
    openTasks=[]
    closedTasks=[]
    
    for task in allTasks:
        if datetime.now(pytz.utc) < task.openTime:  # This is so that tasks that are created before starting time are viewable until then.
            pass
        elif (datetime.now(pytz.utc) >= task.openTime and 
              datetime.now(pytz.utc) <= task.closeTime):  # Or, in other words, if it's during the lifetime of the task.
            openTasks.append(task)
        else:  # If it's after the task has closed, add it to the closedTasks list
            closedTasks.append(task)

    return render_to_response(
        'tasks.html',
        {'openTasks': openTasks, 'closedTasks': closedTasks, 'filtSubs': filtSubs},
        context_instance=RequestContext(request))




@login_required(login_url='/login/')  # This is required until the concept of the Guest view is created so that code won't error.
def uploadFile(request):
    """
    Uploads a submissions file to be viewed on the site
    """

    def postUploadUpdate(upload_instance):
        """
        Will set a mostRecent flag to true to determine a user's most recent submission for each task
        as well as set the uploadURL based on the automatically generated id
        """ 

        sameSubType = Upload.objects.filter(userID=upload_instance.userID, task=upload_instance.task)
        
        for sub in sameSubType: 
            if sub.mostRecent == True:
                sub.mostRecent = False
                sub.save()
        
        upload_instance.mostRecent = True

        upload_instance.uploadURL = '/'.join(['/tasks', str(upload_instance.task.id), str(upload_instance.id)])
        upload_instance.save()

        
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            uploadedFile = request.FILES['fileUpload']
            upload_instance = form.save(commit=False)  # Saves the form but don't commit it since some fields are still empty.
            upload_instance.userID = request.user  # Saves the current user's id to ForeignKey to allow sorting in Tasks view.
            upload_instance.task = Task.objects.get(
                    pk=request.POST['taskID'])  # Save the current task's ID to allow sorting in Tasks view
            userName = str(upload_instance.userID)
            fileName = upload_instance.task.fileName
            uploadContainer = uploadFileName(userName, upload_instance.task, datetime.now())

            try:  
                os.makedirs(os.path.join(settings.MEDIA_ROOT,'file_uploads', userName, uploadContainer))
            except:
                pass    
            
            default_storage.save(os.path.join(settings.MEDIA_ROOT,'file_uploads', userName, uploadContainer, fileName), uploadedFile)  # Save to disc   #changed        
            
            upload_instance.fileUpload = os.path.join(settings.MEDIA_ROOT,'file_uploads', userName, uploadContainer, fileName) # Save to server #changed

            upload_instance.save()
            postUploadUpdate(upload_instance) # post_save method would probably be more appropriate
            
            evaluate(upload_instance) 
            
            return HttpResponseRedirect('/tasks/' + str(upload_instance.task.id) + '/' + str(upload_instance.id))
        else: 
            return HttpResponseRedirect('/tasks/')  # If not valid, reloads task page - eventually may be preventable.
    else:
        form = Upload()
     
    return render_to_response('GameAndGrade_Base_StudentTasks.html', {'form': form})


def uploadCode(request):
    """ 
    Uploads the pasted code as a submissions file to be viewed on the site. Not currently in use
    """
    
    if request.method == 'POST':
        form = UploadCodeForm(dict(request.POST)) # Request File, but not a file/ That's why there's n

        if form.is_valid():
            code = request.POST['code']
            taskID = request.POST['taskID']
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
            
            upload_instance = Upload(userID=user, task=task) #Creating the upload instance
            default_storage.save(path.join(settings.MEDIA_ROOT,'file_uploads', userID, fileName, "prime.py"),ContentFile(code)) #hard-coded file needs to be addressed
            upload_instance.fileUpload = path.join(settings.MEDIA_ROOT, 'file_uploads', userID, fileName, "prime.py")
            upload_instance.save()  # post_save method is called to generate PyLint output from the upload
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


def unitTestEvaluate(evaluators, uploadFilePath):
    """
    The following code will run a series of unit test evaluators that the instructor will have uploaded for the task.       
    """    

    uploadFilePath = uploadFilePath.split('/') # string transformation to generate the necessary path from the given file path
    del uploadFilePath[-1]
    uploadFilePath = '/'.join(uploadFilePath)

    for test in evaluators:
        evalPath = test.file.path
        evalFileName = evalPath.rsplit('/')[-1]
        newEvalPath = os.path.join(uploadFilePath, evalFileName)     
        shutil.copyfile(evalPath, newEvalPath) # copy every test into the upload container
                
        formatterPath = os.path.join(settings.PROJECT_PATH, "unitTestFormatter.py" )
        formatterPath = formatterPath.replace(' ', '\ ') # format everything for the command
        uploadFilePath = uploadFilePath.replace(' ', '\ ') 
        cmdLine = 'python %s %s' % (formatterPath, uploadFilePath)

        cmds = shlex.split(cmdLine)
        p = subprocess.Popen(cmds, cwd = uploadFilePath, 
                             stderr=subprocess.STDOUT, stdout=open(uploadFilePath + "/fsda",'a'))
        
        stdout,stderr = p.communicate()


def evaluate(file_instance):
    """
    Will run Pylint and task-associated unittests against the uploaded file    
    """
    
    evals = UnitTest.objects.filter(tasks=file_instance.task) # discovers the unit tests for the task in question
    uploadFilePath = str(file_instance.fileUpload) # discovers the path for the file in question

    gameAndGradeParser.pylintEvaluate(uploadFilePath)
    unitTestEvaluate(evals, uploadFilePath)
        

@login_required(login_url='/login/')  # This is required until the concept of the Guest view is created so that code won't err.
def viewSub(request, taskID, subID):
    """
    Allows you to view a partcular submission's code and the problems PyLint has found with the code.
    """    
    
    sameSubType = Upload.objects.filter(userID=request.user, task=taskID) 
    # a list that defines submissions that share a tasKID and userID with the submission in question
    sameSubTypeMax = sameSubType.count() - 1

    
    def locateLatestSub(request, sub):
        """
        Navigation function that returns the most recent submission for a task based on the user and submission selected
        """
        
        return sameSubType[sameSubTypeMax]
    
    
    def locateNextSub(request, sub):
        """
        Navigation function that returns the next submission for a task based on the user and submission selected
        """
           
        for counter in range (0, sameSubTypeMax + 1):# cannot use .len() or .index() on this object
            if sameSubType[counter].id == sub.id:
                if counter == sameSubTypeMax:
                    return sameSubType[counter]
                else:
                    return sameSubType[counter + 1]
            
            
    def locatePreviousSub(request, sub):
        """
        Navigation function that returns the previous submission for a task based on the user and submission selected.
        The reverse version of locateNextSub, perhaps this can be refactored?
        """
        
        for counter in range (sameSubTypeMax , -1, -1):# cannot use .len() or .index() on this object
            if sameSubType[counter].id == sub.id:
                if counter == 0:
                    return sameSubType[counter]
                else:
                    return sameSubType[counter - 1]

            
    def locateFirstSub(request, sub):
        """
        Navigation function that returns the first submission for a task based on the user and submission selected
        """
        
        return sameSubType[0]
    
    
    def viewingPermission(request, submission):
        """
        This is a function to prevent users from viewing submissions they did not personally upload.
        It is to be replaced by a system of permissions based on group.
        """
        
        if not request.user.is_staff and not request.user == s.userID:  #and admin/group check
            response = HttpResponse()
            response.status_code = 403
            return response    
        
    s = Upload.objects.get(pk=subID)  # Get the submission that was selected.

        
    viewingPermission(request,s)
    
    codePath = s.fileUpload.path
    
    with open(codePath, mode='r') as f:
        codeString = f.read()
    
    codePath = codePath.split('/')
    del codePath[-1]
    codePath = '/'.join(codePath) # these steps would be more sensible as path transformations, not string
    
    pylintCodePath = codePath + "/pylintOutput.txt"
    unitTestCodePath = codePath + "/log_file.txt"
        
    parsedUnitTest = unitTestParser.parseUnitTestResults(unitTestCodePath)
    parsedPylint = gameAndGradeParser.readable_output(pylintCodePath).replace('\n', '<br>')  
    
    return render_to_response('submissions.html', 
                              {'currSub': codeString, 'subPylint': parsedPylint, 
                               'subUnitTest': parsedUnitTest,'subs': s, 'nextSub': locateNextSub(request,s), 
                               'previousSub': locatePreviousSub(request,s), 'firstSub': locateFirstSub(request,s), 'latestSub': locateLatestSub(request, s)}, 
                                context_instance=RequestContext(request))
