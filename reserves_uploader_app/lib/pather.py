import logging, os, unicodedata

from django.conf import settings

log = logging.getLogger(__name__)


def create_file_url( filename, directories_path ) -> str:
    """ Creates url for file.
        Called by lib/uploader_helper.handle_uploaded_file() """
    log.debug( f'filename, ``{filename}``' )
    log.debug( f'directories_path, ``{directories_path}``' )
    url_directory_path = directories_path.replace( settings.UPLOADS_DIR_PATH, settings.UPLOADS_DIR_URL_ROOT )
    log.debug( f'url_directory_path, ``{url_directory_path}``' )
    file_url = f'{url_directory_path}/{filename}'
    log.debug( f'file_url, ``{file_url}``' )
    return file_url


def normalize_unicode( initial_filename ) -> str:
    """ Normalizes unicode characters by decomposition.
        Called by lib/uploader_helper.handle_uploaded_file(). """
    log.debug( f'initial_filename, ``{initial_filename}``' )
    normalized_filename = unicodedata.normalize( 'NFKD', initial_filename )
    log.debug( f'normalized_filename, ``{normalized_filename}``' )
    evaluation = ( initial_filename == normalized_filename )
    log.debug( f'initial-equals-normalized, ``{evaluation}``' )
    return normalized_filename


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


def create_file_path( filename: str, root_path: str ) -> str:
    """ Creates file path via partial pair-tree structure.
        Example: given a root_path of `/path/to/files`, 
                 if filename is `1234567890.pdf`, 
                 returns `/path/to/files/12/34/1234567890.pdf`. 
        Called by lib/uploader_helper.handle_uploaded_file(). """
    log.debug( f'filename, ``{filename}``' )
    ## handle non-ascii filename ------------------------------------
    pairtree_filepath = ''
    first_four = filename[:4]
    try:
        first_four.encode( 'ascii' )
    except UnicodeEncodeError:
        log.debug( 'first_four contains non-ascii characters' )
        pairtree_filepath = f'{root_path}/unicode/{filename}'
    ## handle ascii filename ----------------------------------------
    if pairtree_filepath == '':
        log.debug( 'filename contains only ascii characters' )
        ( mainpart, extension ) = os.path.splitext( filename )
        if len( mainpart ) < 2:
            pairtree_filepath = f'{root_path}/{filename}'
        elif len(mainpart) >= 2 and len(mainpart) <= 3:
            pairtree_filepath = f'{root_path}/{filename[:2]}/{filename}'
        else:
            pairtree_filepath = f'{root_path}/{filename[:2]}/{filename[2:4]}/{filename}'
    log.debug( f'pairtree_filepath, ``{pairtree_filepath}``' )
    return pairtree_filepath


# def create_file_path( filename: str, root_path: str ) -> str:
#     """ Creates file path via partial pair-tree structure.
#         Example: given a root_path of `/path/to/files`, 
#                  if filename is `1234567890.pdf`, 
#                  returns `/path/to/files/12/34/1234567890.pdf`. 
#         Called by lib/uploader_helper.handle_uploaded_file(). """
#     log.debug( f'filename, ``{filename}``' )
#     ## handle non-ascii filename ------------------------------------
#     pairtree_filepath = ''
#     try:
#         filename.encode( 'ascii' )
#     except UnicodeEncodeError:
#         log.debug( 'filename contains non-ascii characters' )
#         pairtree_filepath = f'{root_path}/unicode/{filename}'
#     ## handle ascii filename ----------------------------------------
#     if pairtree_filepath == '':
#         log.debug( 'filename contains only ascii characters' )
#         ( mainpart, extension ) = os.path.splitext( filename )
#         if len( mainpart ) < 2:
#             pairtree_filepath = f'{root_path}/{filename}'
#         elif len(mainpart) >= 2 and len(mainpart) <= 3:
#             pairtree_filepath = f'{root_path}/{filename[:2]}/{filename}'
#         else:
#             pairtree_filepath = f'{root_path}/{filename[:2]}/{filename[2:4]}/{filename}'
#     log.debug( f'pairtree_filepath, ``{pairtree_filepath}``' )
#     return pairtree_filepath


def create_subdirectories( pairtree_filepath ) -> str:
    """ Creates subdirectories if needed.
        Called by lib/uploader_helper.handle_uploaded_file(). """
    log.debug( f'pairtree_filepath, ``{pairtree_filepath}``' )
    directories_path: str = os.path.dirname( pairtree_filepath )
    log.debug( f'directories_path, ``{directories_path}``' ) 
    if not os.path.exists( directories_path ):
        log.debug( 'directories do not exist' )
        os.makedirs( directories_path )  # creates directories if needed
    else:
        log.debug( 'directories exist' )
    return directories_path
