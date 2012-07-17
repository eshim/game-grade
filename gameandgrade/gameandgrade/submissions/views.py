from gameandgrade.submissions.models import Task, Upload, UserID
from django.contrib.auth.decorators import login_required
from gameandgrade.submissions.upload import UploadForm
from django.contrib.auth import authenticate, logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import RequestContext
from gameandgrade import settings
from gameandgrade import parser
from datetime import datetime
import subprocess
import datetime
import os


# ----------------------------------
# Post-Save Process for Evaluation
#---------------------------------

@receiver(post_save, sender=Upload)
def evaluate(sender, **kwargs):
    inPath = str(kwargs['instance'].fileUpload)
    outPath = inPath.replace("file_uploads","evaluated_code")
    inPath = inPath.replace(" ","\ ")
    
    print "in: " + inPath
    print "out: " + outPath
    
    import shlex
    cmdLine = "pylint --reports=n --include-ids=y --disable=F,I,R,W " + inPath 
    cmds = shlex.split(cmdLine)
    p = subprocess.Popen(cmds,stdout=open(outPath,'w'))
    stdout,stderr = p.communicate()
    
# --------------------------
# View for Uploading Files
#--------------------------

def uploadFile(request):
    from django.core.files.storage import default_storage
    print "got to method"
    if request.method == 'POST':
        print 'Post'
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            print request.FILES
            myFile = request.FILES['fileUpload']
            print "got validated"
            upload_instance = form.save(commit=False)
            upload_instance.userID = request.user
            upload_instance.task = Task.objects.get(pk=request.POST['taskID'])
            print upload_instance.fileUpload
            saveLocation = str(upload_instance.userID)
            try:
                os.makedirs(os.path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation))
            except:
                pass
            try:
                os.makedirs(os.path.join(settings.MEDIA_ROOT,'evaluated_code', saveLocation))
            except:
                pass
            print os.path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation)
            # timestamp = upload_instance.uploadTime.strftime('%a, %d %b, %Y at %I:%M %p')
            fileName = upload_instance.fileName = upload_instance.title
            print upload_instance.fileName
            default_storage.save(os.path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation, fileName),myFile)            
            upload_instance.fileUpload = os.path.join(settings.MEDIA_ROOT,'file_uploads', saveLocation, fileName)
            # Pylinting is done and saved here
            # Ex. Pylint: subprocess.call(pylint --reports=n --include-ids=y <insert filepath here> shell=False)
            upload_instance.save()
            print 'saved'
            return HttpResponseRedirect('/tasks/')
        else: 
            print "got to validation else"
            print form.errors  
    else:
        form = Upload()
    return render_to_response('GameAndGrade_Base_StudentTasks.html', {'form': form})

# ------------------------
# View for Viewing Tasks
#------------------------

@login_required(login_url='/login/')
def tasks(request):
    filtSubs = Upload.objects.filter(userID=request.user).order_by('-uploadTime')
    print 'Filtered Subs', filtSubs
    
    allTasks = Task.objects.all().order_by('-openTime')
    allUploads = Upload.objects.all().order_by('-uploadTime')
    print "All Submissions", allUploads
    openTasks=[]
    closedTasks=[]
    
    for x in allTasks:
        if datetime.datetime.now() < x.openTime:
            pass
        elif datetime.datetime.now() >= x.openTime and datetime.datetime.now() <= x.closeTime:
            openTasks.append(x)
        else:
            closedTasks.append(x)

    return render_to_response(
        'GameAndGrade_Base_StudentTasks.html',
        {'openTasks': openTasks, 'closedTasks': closedTasks, 'filtSubs': filtSubs},
        context_instance=RequestContext(request))
    
# ----------------------
# View for Logging Out
#----------------------
    
def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/tasks') # Note need to change to '/' once we create a home page

# -------------------------------
# View for Viewing a Submission
#-------------------------------

def viewSub(request, subID):
    s = Upload.objects.get(pk=subID)
    currUser = request.user
    print currUser
    fileName = s.title
    print fileName
    codePath = s.fileUpload.path
    print "code path: ", codePath
    evalCodePath = codePath.replace("file_uploads","evaluated_code")
    print "evaluated code path: ", evalCodePath
    f = open(codePath, mode='r')
    subString = f.read()
    f.close()
    print subString
    e = parser.readable_output(evalCodePath)
    e = e.replace('\n', '<br>')
    print e
    return render_to_response('GameAndGrade_Base_StudentTasks_Submissions_SubmissionCode.html', {'currSub': subString, 'evalSub': e}, context_instance=RequestContext(request))