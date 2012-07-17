from django.forms import ModelForm
from gameandgrade.submissions.models import Upload

class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ('fileUpload','title',)