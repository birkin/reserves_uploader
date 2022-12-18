import logging

from django import forms
from django.conf import settings
from django.conf import settings
from django.core.exceptions import ValidationError


log = logging.getLogger(__name__)


class UploadFileForm(forms.Form):
    file = forms.FileField()
    # file = forms.FileField( upload_to=settings.UPLOADS_DIR_PATH )

    # def clean_filename(self):
    def clean(self):
        log.debug( 'starting clean()' )
        log.debug( f'self.cleaned_data, ``{self.cleaned_data}``' )
        filename = self.cleaned_data["file"].name
        for prohibited_character in settings.PROHIBITED_CHARACTERS:
            if prohibited_character in filename:
                msg = f'filename contains prohibited character: ``{prohibited_character}``'
                log.debug( msg )
                raise ValidationError( msg )
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        log.debug( 'filename apparently valid' )
        return filename

    # def clean_recipients(self):
    #     data = self.cleaned_data['recipients']
    #     if "fred@example.com" not in data:
    #         raise ValidationError("You have forgotten about Fred!")

    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
    #     return data
