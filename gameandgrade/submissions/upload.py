from django.forms                    import ModelForm
from django 			             import forms 
from gameandgrade.submissions.models import Upload

class UploadForm(ModelForm):
    """
    This generates an upload form from the upload model to allow users to submit their uploads
    """
    
    class Meta:
        # There is only one field to be validated because other fields are to be modified after the validation
        model = Upload
        fields = ('fileUpload',)

class UploadCodeForm(forms.Form):
    title = forms.CharField(max_length=100)
    code = forms.CharField()
    taskID = forms.CharField()

