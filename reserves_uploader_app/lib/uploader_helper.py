import datetime, logging, os, pprint

import requests
from django.conf import settings
from django.core.cache import cache


log = logging.getLogger(__name__)


## GET helpers ------------------------------------------------------


def build_uploader_GET_context( session_message: str ) -> dict:
    """ Builds context for the uploader page.
        Called by views.uploader() """
    log.debug( f'session_message, ``{session_message}``' )
    context = {
        'error_message': '',
        'success_message': '',
        'pattern_header': '',
        'prohibited_characters': ''
    }
    prohibited_characters_string = ', '.join( settings.PROHIBITED_CHARACTERS )
    log.debug( f'prohibited_characters_string, ``{prohibited_characters_string}``')
    context['prohibited_characters'] = prohibited_characters_string
    pattern_header_html: str = prep_pattern_header_html()
    context['pattern_header'] = pattern_header_html
    if 'success' in repr( session_message ):
        context['success_message'] = session_message
        context['error_message'] = ''
    elif 'error' in repr( session_message ):
        context['success_message'] = ''
        context['error_message'] = session_message
    log.debug( f'context for GET, ``{pprint.pformat(context)[0:500]}``' )
    # log.debug( f'context.keys(), ``{pprint.pformat(context.keys())}``' )
    log.debug( f'context["error_message"], ``{context["error_message"]}``' )
    log.debug( f'context["success_message"], ``{context["success_message"]}``' )
    return context


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


## POST helpers ------------------------------------------------------


def handle_uploaded_file(f):
    """ Handle uploaded file without overwriting pre-existing file. """
    log.debug( 'starting handle_uploaded_file()' )
    full_file_path = f'{settings.UPLOADS_DIR_PATH}/{f.name}'
    if os.path.exists( full_file_path ):
        log.debug( 'file exists; appending timestamp' )
        timestamp = datetime.datetime.now().strftime( '%Y-%m-%d_%H-%M-%S' )
        full_file_path = f'{settings.UPLOADS_DIR_PATH}/{f.name}_{timestamp}'
    log.debug( f'full_file_path, ``{full_file_path}``' )
    with open( full_file_path, 'wb+' ) as destination:
        log.debug( 'starting write' )
        for chunk in f.chunks():
            destination.write(chunk)
    log.debug( f'writing finished' )
    return
