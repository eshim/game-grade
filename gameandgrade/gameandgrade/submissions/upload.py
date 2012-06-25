from django import forms

class UploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    fileUpload  = forms.FileField()