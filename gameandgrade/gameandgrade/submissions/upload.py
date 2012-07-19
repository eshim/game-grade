from django.forms                    import ModelForm
from gameandgrade.submissions.models import Upload

class UploadForm(ModelForm):
    """
    This generates an upload form from the upload model to allow users to submit their uploads
    """
    
    class Meta:
        # There are only two fields to be validated because other fields are to be modified after the validation
        model = Upload
        fields = ('fileUpload','title',) 