from gameandgrade.submissions.models import Task, Exercise
from django.contrib import admin
from django.contrib.admin import BooleanFieldListFilter

class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 2

class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Task Information', {'fields': ['descrip', 'xpVal', 'openTime', 'closeTime']}),
    ]
    inlines = [ExerciseInline]
    list_display = ('title', 'openTime', 'closeTime', 'isOpen')
    list_filter = ('openTime',)

admin.site.register(Task, TaskAdmin)