import logging

from django import forms
from django.conf import settings
from django.conf import settings
from django.core.exceptions import ValidationError


log = logging.getLogger(__name__)


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean(self):
        log.debug( 'starting clean()' )
        log.debug( f'self.cleaned_data, ``{self.cleaned_data}``' )
        try:
            filename = self.cleaned_data["file"].name
        except:
            msg = 'error: no file selected'
            log.debug( msg )
            raise ValidationError( msg )
        bad_characters = []
        bad_character_string = ''
        for prohibited_character in settings.PROHIBITED_CHARACTERS:
            if prohibited_character in filename:
                bad_characters.append( prohibited_character )
        if len( bad_characters ) > 0:
            bad_character_string = ', '.join( bad_characters )
            msg = f'error: prohibited filename characters: {bad_character_string}'
            log.debug( msg )
            raise ValidationError( msg )
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        log.debug( 'filename apparently valid' )
        return filename

    # def clean(self):
    #     log.debug( 'starting clean()' )
    #     log.debug( f'self.cleaned_data, ``{self.cleaned_data}``' )
    #     filename = self.cleaned_data["file"].name
    #     bad_characters = []
    #     bad_character_string = ''
    #     for prohibited_character in settings.PROHIBITED_CHARACTERS:
    #         if prohibited_character in filename:
    #             bad_characters.append( prohibited_character )
    #     if len( bad_characters ) > 0:
    #         bad_character_string = ', '.join( bad_characters )
    #         msg = f'error: prohibited filename characters: {bad_character_string}'
    #         log.debug( msg )
    #         raise ValidationError( msg )
    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
    #     log.debug( 'filename apparently valid' )
    #     return filename

    ## end class UploadFileForm()
