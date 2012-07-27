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

from django.contrib.auth.models      import User
from gameandgrade                    import settings
from datetime                        import datetime

from subprocess                      import Popen, PIPE
from shlex                           import split
from os                              import makedirs, path

    
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
                makedirs(path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation))
            except:
                pass
            try:  # Try to make a directory with user's name if not created for PyLint output.
                makedirs(path.join(settings.MEDIA_ROOT,'evaluated_code/pylint', saveLocation))
            except:
                pass
            try:
                makedirs(path.join(settings.MEDIA_ROOT,'evaluated_code/unit_tests', saveLocation))
            except:
                pass
            
            fileName = upload_instance.title  # This is what the uploaded file's name will be.
            default_storage.save(path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation, fileName),myFile)  # Save to disc          
            upload_instance.fileUpload = path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation, fileName)
            upload_instance.save()  # post_save method is called to generate PyLint output from the uploaded file.
            
            setMostRecent(upload_instance)
            
            return HttpResponseRedirect('/tasks/')
        else: 
            return HttpResponseRedirect('/tasks/')  # If not valid, reloads task page - eventually may be preventable.
    else:
        form = Upload()
    
    return render_to_response('GameAndGrade_Base_StudentTasks.html', {'form': form})


@receiver(post_save, sender=Upload)  # When an Upload object is saved, also do the following function
def evaluate(sender, **kwargs):
    """
<<<<<<< HEAD
    Will generate a PyLint output file that evaluates an uploaded file, and a Unit Test file checking code against requirements.    """
    
    evals = UnitTest.objects.get(tasks=kwargs['instance'].task)
=======
    Will generate a PyLint output file that evaluates an uploaded file, and a Unit Test file checking code against requirements.
    """
    
    evals = UnitTest.objects.filter(tasks=kwargs['instance'].task)
>>>>>>> fminio
    print 'evals', evals
    inPath = str(kwargs['instance'].fileUpload)  # The path to the user's uploaded code
    print "in_orig", inPath
    outPathLint = inPath.replace('file_uploads','evaluated_code/pylint')  # The path to the generated PyLint output
    outPathTest = inPath.replace('file_uploads', 'evaluated_code/unit_tests')
    print "out pylint", outPathLint
    print "out unit tests", outPathTest
    inPath = inPath.replace(' ','\ ')  # This prevents spaces in the inpath from becoming individual shell commands
    print "in_new", inPath
    cmdLine = 'pylint --reports=n --include-ids=y --disable=F,I,R,W ' + inPath  # Builds the command to be run by the shell 
    cmds = split(cmdLine)  # This makes the commands above readable to the shell.
    print "cmds", cmds
    p = Popen(cmds,stdout=open(outPathLint,'w'))  # This executes the command created and saves output
<<<<<<< HEAD
    stdout,stderr = p.communicate()  # Sends output to stdout to be saved.
    
    evalPath = evals.file.path
    evalPath = evalPath.replace(' ', '\ ')
    print "evalPath",evalPath
    cmdLine = 'python %s' % (evalPath)
    cmds = split(cmdLine)
    print "cmds", cmds
    p = Popen(cmds,stderr=open(outPathTest,'w'))  # This executes the command created and saves output
=======
>>>>>>> fminio
    stdout,stderr = p.communicate()  # Sends output to stdout to be saved.
    
    for test in evals:
        evalPath = test.file.path
        evalPath = evalPath.replace(' ', '\ ')
        print "evalPath",evalPath
        cmdLine = 'python %s' % (evalPath)
        cmds = split(cmdLine)
        print "cmds", cmds
        p = Popen(cmds,stderr=open(outPathTest,'a'))  # This executes the command created and saves output
        stdout,stderr = p.communicate()  # Sends output to stdout to be saved.


@login_required(login_url='/login/')  # This is required until the concept of the Guest view is created so that code won't error.
def viewSub(request, subID):
    """
    Allows you to view a partcular submission's code and the problems PyLint has found with the code.
    """
    
    s = Upload.objects.get(pk=subID)  # Get the submission that was selected.
    currUser = request.user
    codePath = s.fileUpload.path
    evalCodePath = codePath.replace("file_uploads","evaluated_code/pylint")  # This works since the only difference in paths are this.
    
    with open(codePath, mode='r') as f:
        subString = f.read()    
    
    e = parser.readable_output(evalCodePath)  # Sends path to PyLint file to parser file to make user output user friendly.
    e = e.replace('\n', '<br>')  # Replaces all newline characters with a break tag for formatting -- TO BE CHANGED LATER?
    
    return render_to_response('GameAndGrade_Base_StudentTasks_Submissions_SubmissionCode.html', 
                              {'currSub': subString, 'evalSub': e, 'subs': s}, context_instance=RequestContext(request))