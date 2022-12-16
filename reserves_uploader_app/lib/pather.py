import logging

from django.conf import settings

log = logging.getLogger(__name__)


def is_valid_filename( filename ) -> dict:
    """ Checks that filename is valid for server. """
    log.debug( f'filename, ``{filename}``' )
    log.debug( f'len(filename), ``{len(filename)}``' )
    assert type(filename) == str
    prohibited_characters = settings.PROHIBITED_CHARACTERS
    log.debug( f'sorted(prohibited_characters), ``{sorted(prohibited_characters)}``' )
    assessment = { 'valid': False, 'err': None}
    filename = filename.strip( ' ' )
    if len(filename) == 0:
        assessment['err'] = 'filename is empty'
    elif filename.startswith( '.' ):
        assessment['err'] = 'filename starts with a period'
    elif ' ' in filename:
        assessment['err'] = 'filename contains a space'
    elif len(filename) > 100:
        assessment['err'] = 'filename is too long'
    elif any( [ char in filename for char in prohibited_characters ] ):
        assessment['err'] = 'filename contains a prohibited character'
    else:
        assessment['valid'] = True
    log.debug( f'assessment, ``{assessment}``' )
    return assessment


def create_file_path( filename, root_path ):
    """ Creates file path via partial pair-tree structure.
        Example: given a root_path of `/path/to/files`, 
                 if filename is `1234567890.pdf`, 
                 returns `/path/to/files/12/34/1234567890.pdf`. """
    log.debug( f'filename, ``{filename}``' )
    ## strip leading '.' and spaces from filename ------------------
    filename = filename.lstrip( ' ' )
    if filename.startswith( '.' ):
        filename = filename[1:]
    filename = filename.strip( ' ' )
    filename = filename.replace( ' ', '_' )
    ## create file_path ---------------------------------------------
    filepath = f'{root_path}/{filename[:2]}/{filename[2:4]}/{filename}'
    return filepath