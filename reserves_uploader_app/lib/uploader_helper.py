import logging, pprint

log = logging.getLogger(__name__)


def build_uploader_GET_context() -> dict:
    """ Builds context for the uploader page.
        Called by views.uploader() """
    log.debug( 'starting' )
    context = {}
    pattern_header_html: str = prep_pattern_header_html()
    context['pattern_header'] = pattern_header_html
    log.debug( f'context, ``{pprint.pformat(context)}``' )
    return context

def prep_pattern_header_html() -> str:
    return ''