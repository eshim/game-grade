from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from gameandgrade.submissions.upload import UploadForm
from gameandgrade.submissions.models import Task, Submission, Upload
from gameandgrade.submissions.newTaskForm import TaskForm
import datetime
import os
from gameandgrade import settings

# -------------------------------------------------
# Importing for template context for static files
#-------------------------------------------------
from django.template import RequestContext

# --------------------------
# View for Uploading Files
#--------------------------


def uploadFile(request):
    print "got to method"
    if request.method == 'POST':
        print "got to post method"
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            print "got validated"
            new_upload = Upload(title=request.POST['title'], 
                                fileUpload=request.FILES['fileUpload'])
            new_upload.save()
            return HttpResponseRedirect('/tasks/')
        else: 
            print "got to validation else"
            print form.errors  
    else:
        form = Upload()
    return render_to_response('GameAndGrade_Base_StudentTasks.html', {'form': form})

def allTasks(request):
   
# ------------------------------------------------------------------------------------------------
# This creates a fake user. THIS CODE IS A HACK, REMOVE WHEN ACTUALLY CREATING LEGITMITATE USERS
#------------------------------------------------------------------------------------------------
#    username = "fakeUser"
##    Put plaintext password in method
##    password = hashers.make_password('')
##    just try plaintext password
#    password = 'flower10'
#    user = authenticate(username=username, password=password)
#    request.user.id = user.id
    
# -------------------------------------
# Miscellaneous testing for fake user
#-------------------------------------
    
#    if user is not None:
#        #It worked
#        print "Worked"
#        print user.username
#    else:
#        print "Didn't work"     
#    taskDict = defaultdict(list)
#    for t in Task.objects.all():
#        taskDict[t.id].append(t)
#        taskDict[t.id].append(datetime.datetime.now() < t.closeTime)
#        taskDict[t.id].append(Submission.objects.filter(taskID=t.id, userID = request.user.id))  
#    return render_to_response('GameAndGrade_Base_StudentTasks.html', {'taskDict':taskDict})

# ----------------------------------------------------------------------------------------
# This is my working code that sends the task and submissions to the template.
#----------------------------------------------------------------------------------------
    allTasks = Task.objects.all().order_by('-openTime')
    allUploads = Upload.objects.all()
    openTasks=[]
    closedTasks=[]
    subs={}
    
    for x in allTasks:
        if datetime.datetime.now() < x.openTime:
            pass
        elif datetime.datetime.now() >= x.openTime and datetime.datetime.now() <= x.closeTime:
            openTasks.append(x)
        else:
            closedTasks.append(x)
            
        if datetime.datetime.now() >= x.openTime:
            if x.id not in subs.keys() and len(Submission.objects.filter(taskID=x.id, userID = request.user.id)) != 0:
                y = Submission.objects.filter(taskID=x.id, userID = request.user.id)
                subs[x.id] = y
    
# Sending the whole thing, including filtered subs

#    return render_to_response(
#        'GameAndGrade_Base.html',
#        {'openTasks': openTasks, 'closedTasks': closedTasks, 'subs': subs},
#        context_instance=RequestContext(request))

#Sending a fake thing, unfiltered subs to see if it works.

    return render_to_response(
        'GameAndGrade_Base_StudentTasks.html',
        {'openTasks': openTasks, 'closedTasks': closedTasks, 'allUploads': allUploads},
        context_instance=RequestContext(request))
    
#Crappy customizable template for login. Hopefully will be gone.
    
#def login_user(request):
#    state = "Please log in below..."
#    username = password = ''
#    if request.POST:
#        username = request.POST.get('username')
#        password = request.POST.get('password')
#
#        user = authenticate(username=username, password=password)
#        if user is not None:
#            login(request, user)
#            state = "Welcome back, %s!" % (username)
#        else:
#            state = "Invalid username/password combination."
#    return render_to_response('GameAndGrade_Base_Login.html',{'state':state, 'username': username})

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/tasks') #Note need to change to '/' once we create a home page

def createTask(request):
    if request.method == 'POST':
        print "got to post"
        form = TaskForm(request.POST)
        if form.is_valid():
            print "valid!"
            form.save()
            print "saved!"
            return HttpResponseRedirect('/tasks/')
        else:
            print "invalid! errors are:"
            print form.errors
    else:
        print "unbound form"
        form = TaskForm()
    return render_to_response('GameAndGrade_Base_newTask.html', {'form':form}, context_instance=RequestContext(request))