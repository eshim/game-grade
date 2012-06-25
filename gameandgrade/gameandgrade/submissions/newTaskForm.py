from django.forms import ModelForm
from gameandgrade.submissions.models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task