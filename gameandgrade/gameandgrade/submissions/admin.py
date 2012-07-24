from gameandgrade.submissions        import models 
from django.contrib                  import admin
from django.contrib.admin            import BooleanFieldListFilter
from os                              import makedirs, path
from shutil                          import copyfile
from gameandgrade.settings           import MEDIA_ROOT
from cStringIO                       import StringIO
from django.http                     import HttpResponse
from datetime                        import datetime
from StringIO                        import StringIO  
from zipfile                         import ZipFile, ZIP_DEFLATED


class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None,               {'fields': ['title']}),
                 ('Task Information', {'fields': ['descrip', 'xpVal', 'openTime', 'closeTime']}),
                 ]
    list_display = ['title', 'openTime', 'closeTime', 'isOpen']
    list_filter = ['openTime']
    search_fields = ['title']
    
    
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'tags']
    search_fields = ['tags']
    
    
class UserAdmin(admin.ModelAdmin):
    model = models.UserID
    

class UploadAdmin(admin.ModelAdmin):
    def downloadUploads(self, request, queryset):
        response = HttpResponse(mimetype='application/zip', content_type='application/zip')
        username = str(request.user)
        filename = '%s_%s' % (username, datetime.now().strftime('%H%M%S%f'))
        response['Content-Disposition'] = 'filename=%s.zip' % (filename)
        print 'username:', username
        print 'filename', filename
        
        in_memory = StringIO()  
        zip = ZipFile(in_memory, "a", ZIP_DEFLATED)  
        
        for obj in queryset: #It does get the object I want
            fileObj = open(obj.fileUpload.path, 'r')
            archive = zip.writestr(obj.title, fileObj.read())
            fileObj.close
            for file in zip.filelist:  
                file.create_system = 0 

        zip.close()
        in_memory.seek(0)
        response.write(in_memory.read())
        return response
    
    downloadUploads.short_description = 'Download selected files'
    
    list_display = ['title', 'task', 'userID', 'uploadTime']
    list_filter = ['task', 'userID', 'mostRecent']
    actions = [downloadUploads]
             
#################################################################################################################
# WARNING: Buggy Code Below - Trying to Change Default Filter. Currently requires two clicks to switch to 'All.'
#################################################################################################################
    
    def changelist_view(self, request, extra_context=None):
        if (
            ('HTTP_REFERER' in request.META) and 
            (request.META['HTTP_REFERER'].find('?') == -1) and 
            (not request.GET.has_key('mostRecent__exact'))
        ):
            q = request.GET.copy()
            q['mostRecent__exact'] = '1'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super(UploadAdmin,self).changelist_view(request, extra_context=extra_context)
#################################################################################################################


class UnitTestAdmin(admin.ModelAdmin):
    fieldsets = [
                 (None,               {'fields': ['name', 'file']}),
                 ('Tasks That Will Use This Evaluator', {'fields': ['tasks']}),
                 ]
    list_display = ['name',]
    list_filter = ['tasks']
    search_fields = ['name']

admin.site.register(models.Task, TaskAdmin)

admin.site.register(models.Exercise, ExerciseAdmin)

admin.site.register(models.Upload, UploadAdmin)

admin.site.register(models.UserID, UserAdmin)

admin.site.register(models.UnitTest, UnitTestAdmin)