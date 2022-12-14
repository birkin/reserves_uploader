from django import forms
from django.conf import settings


class UploadFileForm(forms.Form):
    file = forms.FileField()
    # file = forms.FileField( upload_to=settings.UPLOADS_DIR_PATH )
