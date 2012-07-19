from gameandgrade.submissions.models import Task, Exercise, UserID, Upload
from django.contrib                  import admin
from django.contrib.admin            import BooleanFieldListFilter

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
    model = UserID

class UploadAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'userID', 'uploadTime']
    list_filter = ['task', 'userID', 'mostRecent']
     
##################################################################################################
# WARNING: Buggy Code Below - Trying to Change Default Filter
#################################################################################################
    
#    def changelist_view(self, request, extra_context=None):
#        if not request.GET.has_key('mostRecent__exact'):
#
#            q = request.GET.copy()
#            q['mostRecent__exact'] = '1'
#            request.GET = q
#            request.META['QUERY_STRING'] = request.GET.urlencode()
#        return super(UploadAdmin,self).changelist_view(request, extra_context=extra_context)
################################################################################################

admin.site.register(Task, TaskAdmin)

admin.site.register(Exercise, ExerciseAdmin)

admin.site.register(Upload, UploadAdmin)

admin.site.register(UserID, UserAdmin)