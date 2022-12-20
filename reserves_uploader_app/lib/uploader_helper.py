import datetime, logging, os, pprint

import requests
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from reserves_uploader_app.lib import pather


log = logging.getLogger(__name__)


## GET helpers ------------------------------------------------------


def build_uploader_GET_context( session_error_message: str, session_success_message: str ) -> dict:
    """ Builds context for the uploader page.
        Called by views.uploader() """
    # log.debug( f'session_message, ``{session_message}``' )
    log.debug( f'session_error_message, ``{session_error_message}``' )
    log.debug( f'session_success_message, ``{session_success_message}``' )
    context = {
        'error_message': '',
        'success_message': '',
        'pattern_header': '',
        'prohibited_characters': '',
        'form_post_url': '',
    }
    ## add prohibited characters to context -------------------------
    prohibited_characters_string = ', '.join( settings.PROHIBITED_CHARACTERS )
    log.debug( f'prohibited_characters_string, ``{prohibited_characters_string}``')
    context['prohibited_characters'] = prohibited_characters_string
    ## add pattern-header to context --------------------------------
    pattern_header_html: str = prep_pattern_header_html()
    context['pattern_header'] = pattern_header_html
    ## add error and success messages to context --------------------
    context['error_message'] = session_error_message
    context['success_message'] = session_success_message
    # if 'uploaded' in repr( session_message ):
    #     context['success_message'] = session_message
    #     context['error_message'] = ''
    # elif 'error' in repr( session_message ):
    #     context['success_message'] = ''
    #     context['error_message'] = session_message
    ## add form-post-url to context ---------------------------------
    uploader_url = reverse( 'uploader_url' )
    context['uploader_url'] = uploader_url
    ## return context -----------------------------------------------
    log.debug( f'context for GET, ``{pprint.pformat(context)[0:500]}``' )
    # log.debug( f'context.keys(), ``{pprint.pformat(context.keys())}``' )
    log.debug( f'context["error_message"], ``{context["error_message"]}``' )
    log.debug( f'context["success_message"], ``{context["success_message"]}``' )
    return context


# def build_uploader_GET_context( session_message: str ) -> dict:
#     """ Builds context for the uploader page.
#         Called by views.uploader() """
#     log.debug( f'session_message, ``{session_message}``' )
#     context = {
#         'error_message': '',
#         'success_message': '',
#         'pattern_header': '',
#         'prohibited_characters': '',
#         'form_post_url': ''
#     }
#     ## add prohibited characters to context -------------------------
#     prohibited_characters_string = ', '.join( settings.PROHIBITED_CHARACTERS )
#     log.debug( f'prohibited_characters_string, ``{prohibited_characters_string}``')
#     context['prohibited_characters'] = prohibited_characters_string
#     ## add pattern-header to context --------------------------------
#     pattern_header_html: str = prep_pattern_header_html()
#     context['pattern_header'] = pattern_header_html
#     ## add error and success messages to context --------------------
#     if 'uploaded' in repr( session_message ):
#         context['success_message'] = session_message
#         context['error_message'] = ''
#     elif 'error' in repr( session_message ):
#         context['success_message'] = ''
#         context['error_message'] = session_message
#     ## add form-post-url to context ---------------------------------
#     uploader_url = reverse( 'uploader_url' )
#     context['uploader_url'] = uploader_url
#     ## return context -----------------------------------------------
#     log.debug( f'context for GET, ``{pprint.pformat(context)[0:500]}``' )
#     # log.debug( f'context.keys(), ``{pprint.pformat(context.keys())}``' )
#     log.debug( f'context["error_message"], ``{context["error_message"]}``' )
#     log.debug( f'context["success_message"], ``{context["success_message"]}``' )
#     return context


def prep_pattern_header_html() -> str:
    """ Builds pattern-header html.
        Called by build_uploader_GET_context() """
    log.debug( 'starting' )
    cache_key = 'pattern_header'
    header_html = cache.get( cache_key, None )
    if header_html:
        log.debug( 'header in cache' )
    else:
        log.debug( 'header not in cache' )
        r = requests.get( settings.PATTERN_LIB_HEADER_URL )
        header_html: str = r.content.decode( 'utf8' )
        cache.set( cache_key, header_html, settings.PATTERN_LIB_CACHE_TIMEOUT )
    log.debug( f'header_html, ``{header_html[0:500]}``' )
    return header_html


## POST helper ------------------------------------------------------


def handle_uploaded_file( f ) -> str:
    """ Handle uploaded file without overwriting pre-existing file. 
        Called by views.uploader() """
    log.debug( 'starting handle_uploaded_file()' )
    ## get filename -------------------------------------------------
    filename = f.name
    log.debug( f'filename initially, ``{filename}``' )
    ## run unicode-normalizer ---------------------------------------
    filename: str = pather.normalize_unicode( filename )
    ## get pairtree filepath ----------------------------------------
    pairtree_filepath = pather.create_file_path( filename, settings.UPLOADS_DIR_PATH )
    assert settings.UPLOADS_DIR_PATH in pairtree_filepath  # sanity check
    ## create necessary directories ---------------------------------
    pather.create_subdirectories( pairtree_filepath )
    # full_file_path = f'{settings.UPLOADS_DIR_PATH}/{filename}'
    ## add timestamp if file exists ---------------------------------
    # if os.path.exists( full_file_path ):
    if os.path.exists( pairtree_filepath ):
        log.debug( 'file exists; appending timestamp' )
        timestamp = datetime.datetime.now().strftime( '%Y-%m-%d_%H-%M-%S' )
        ( mainpart, extension ) = os.path.splitext( filename )
        if extension:
            filename = f'{mainpart}_{timestamp}{extension}'
        pairtree_filepath = f'{settings.UPLOADS_DIR_PATH}/{filename}'
    log.debug( f'pairtree_filepath, ``{pairtree_filepath}``' )
    with open( pairtree_filepath, 'wb+' ) as destination:
        log.debug( 'starting write' )
        for chunk in f.chunks():
            destination.write(chunk)
    log.debug( f'writing finished' )
    log.debug( f'filename now, ``{filename}``' )
    return filename


# def handle_uploaded_file( f ) -> str:
#     """ Handle uploaded file without overwriting pre-existing file. 
#         Called by views.uploader() """
#     log.debug( 'starting handle_uploaded_file()' )
#     filename = f.name
#     log.debug( f'filename initially, ``{filename}``' )
#     full_file_path = f'{settings.UPLOADS_DIR_PATH}/{filename}'
#     if os.path.exists( full_file_path ):
#         log.debug( 'file exists; appending timestamp' )
#         timestamp = datetime.datetime.now().strftime( '%Y-%m-%d_%H-%M-%S' )
#         ( mainpart, extension ) = os.path.splitext( filename )
#         if extension:
#             filename = f'{mainpart}_{timestamp}{extension}'
#         full_file_path = f'{settings.UPLOADS_DIR_PATH}/{filename}'
#     log.debug( f'full_file_path, ``{full_file_path}``' )
#     with open( full_file_path, 'wb+' ) as destination:
#         log.debug( 'starting write' )
#         for chunk in f.chunks():
#             destination.write(chunk)
#     log.debug( f'writing finished' )
#     log.debug( f'filename now, ``{filename}``' )
#     return filename
