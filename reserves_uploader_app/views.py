import datetime, json, logging, os, pprint

import trio
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from reserves_uploader_app.forms import UploadFileForm
from reserves_uploader_app.lib import uploader_helper
from reserves_uploader_app.lib import version_helper
from reserves_uploader_app.lib.version_helper import GatherCommitAndBranchData

log = logging.getLogger(__name__)


# -------------------------------------------------------------------
# main urls
# -------------------------------------------------------------------


def info(request):
    return HttpResponseRedirect( reverse('version_url') )


@ensure_csrf_cookie
def uploader(request):
    log.debug( 'starting uploader()' )
    # log.debug( f'inital incoming request.session.keys(), ``{pprint.pformat(request.session.keys())}``' )
    if request.method == 'POST':
        log.debug( 'POST detected' )
        log.debug( f'request.POST, ``{pprint.pformat(request.POST)}``' )
        log.debug( f'request.FILES, ``{pprint.pformat(request.FILES)}``' )
        log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
        # assert request.session['msg'] == ''
        assert request.session['session_error_message'] == ''
        assert request.session['session_success_message'] == ''
        log.debug( 'about to instantiate form' )
        form = UploadFileForm(request.POST, request.FILES)
        log.debug( f'form.__dict__, ``{pprint.pformat(form.__dict__)}``' )
        if form.is_valid():
            log.debug( 'form is valid' )
            log.debug( f'form.cleaned_data, ``{pprint.pformat(form.cleaned_data)}``' )
            # filename = uploader_helper.handle_uploaded_file( request.FILES['file'] )  # if duplicate, will have timestamp appended
            url_and_name_dict: dict = uploader_helper.handle_uploaded_file( request.FILES['file'] )  # if duplicate, will have timestamp appended
            filename = url_and_name_dict['filename']
            file_url = url_and_name_dict['file_url']
            # file_url = f'{settings.UPLOADS_DIR_URL_ROOT}/{filename}'
            msg = f'File uploaded; link: <a href="{file_url}">{filename}</a>'
            request.session['session_success_message'] = msg
            log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
        else:
            log.debug( 'form not valid' )
            log.debug( f'form.errors, ``{pprint.pformat(form.errors)}``' )
            log.debug( f'form.non_field_errors(), ``{pprint.pformat(form.non_field_errors())}``' )
            msg: str = form.non_field_errors()[0]
            log.debug( f'error_message, ``{pprint.pformat( msg )}``' )
            # request.session['msg'] = error_message
            request.session['session_error_message'] = msg
        log.debug( 'POST handled, about to redirect' )
        log.debug( f'at end of POST; request.session.keys(), ``{pprint.pformat(request.session.keys())}``' )
        # log.debug( f'at end of POST; request.session["msg"], ``{pprint.pformat(request.session["msg"])}``' )
        log.debug( f'at end of POST; request.session["session_success_message"], ``{pprint.pformat(request.session["session_success_message"])}``' )
        log.debug( f'at end of POST; request.session["session_error_message"], ``{pprint.pformat(request.session["session_error_message"])}``' )
        resp = HttpResponseRedirect( reverse('uploader_url') )  ## TODO, add message as querystring, then display it
    elif request.method == 'GET':
        log.debug( 'GET detected' )
        log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
        ## get any session messages ---------------------------------
        # session_message = request.session.get('msg', '')
        session_error_message = request.session.get('session_error_message', '')
        session_success_message = request.session.get('session_success_message', '')
        # log.debug( f'session_message, ``{session_message}``' )
        log.debug( f'session_error_message, ``{session_error_message}``' )
        log.debug( f'session_success_message, ``{session_success_message}``' )
        ## clear out session message --------------------------------
        # request.session['msg'] = ''
        request.session['session_error_message'] = ''
        request.session['session_success_message'] = ''
        # context: dict = uploader_helper.build_uploader_GET_context( session_message )
        context: dict = uploader_helper.build_uploader_GET_context( session_error_message, session_success_message )
        resp = render( request, 'single_file.html', context )
    else:
        resp = HttpResponseBadRequest( 'bad request' )
    return resp

# @ensure_csrf_cookie
# def uploader(request):
#     log.debug( 'starting uploader()' )
#     # log.debug( f'inital incoming request.session.keys(), ``{pprint.pformat(request.session.keys())}``' )
#     if request.method == 'POST':
#         log.debug( 'POST detected' )
#         log.debug( f'request.POST, ``{pprint.pformat(request.POST)}``' )
#         log.debug( f'request.FILES, ``{pprint.pformat(request.FILES)}``' )
#         log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
#         # assert request.session['msg'] == ''
#         assert request.session['session_error_message'] == ''
#         assert request.session['session_success_message'] == ''
#         log.debug( 'about to instantiate form' )
#         form = UploadFileForm(request.POST, request.FILES)
#         log.debug( f'form.__dict__, ``{pprint.pformat(form.__dict__)}``' )
#         if form.is_valid():
#             log.debug( 'form is valid' )
#             log.debug( f'form.cleaned_data, ``{pprint.pformat(form.cleaned_data)}``' )
#             filename = uploader_helper.handle_uploaded_file( request.FILES['file'] )  # if duplicate, will have timestamp appended
#             file_url = f'{settings.UPLOADS_DIR_URL_ROOT}/{filename}'
#             msg = f'File uploaded; link: <a href="{file_url}">{filename}</a>'
#             request.session['session_success_message'] = msg
#             log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
#         else:
#             log.debug( 'form not valid' )
#             log.debug( f'form.errors, ``{pprint.pformat(form.errors)}``' )
#             log.debug( f'form.non_field_errors(), ``{pprint.pformat(form.non_field_errors())}``' )
#             msg: str = form.non_field_errors()[0]
#             log.debug( f'error_message, ``{pprint.pformat( msg )}``' )
#             # request.session['msg'] = error_message
#             request.session['session_error_message'] = msg
#         log.debug( 'POST handled, about to redirect' )
#         log.debug( f'at end of POST; request.session.keys(), ``{pprint.pformat(request.session.keys())}``' )
#         # log.debug( f'at end of POST; request.session["msg"], ``{pprint.pformat(request.session["msg"])}``' )
#         log.debug( f'at end of POST; request.session["session_success_message"], ``{pprint.pformat(request.session["session_success_message"])}``' )
#         log.debug( f'at end of POST; request.session["session_error_message"], ``{pprint.pformat(request.session["session_error_message"])}``' )
#         resp = HttpResponseRedirect( reverse('uploader_url') )  ## TODO, add message as querystring, then display it
#     elif request.method == 'GET':
#         log.debug( 'GET detected' )
#         log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
#         ## get any session messages ---------------------------------
#         # session_message = request.session.get('msg', '')
#         session_error_message = request.session.get('session_error_message', '')
#         session_success_message = request.session.get('session_success_message', '')
#         # log.debug( f'session_message, ``{session_message}``' )
#         log.debug( f'session_error_message, ``{session_error_message}``' )
#         log.debug( f'session_success_message, ``{session_success_message}``' )
#         ## clear out session message --------------------------------
#         # request.session['msg'] = ''
#         request.session['session_error_message'] = ''
#         request.session['session_success_message'] = ''
#         # context: dict = uploader_helper.build_uploader_GET_context( session_message )
#         context: dict = uploader_helper.build_uploader_GET_context( session_error_message, session_success_message )
#         resp = render( request, 'single_file.html', context )
#     else:
#         resp = HttpResponseBadRequest( 'bad request' )
#     return resp


# -------------------------------------------------------------------
# support urls
# -------------------------------------------------------------------


def error_check( request ):
    """ For an easy way to check that admins receive error-emails (in development)...
        To view error-emails in runserver-development:
        - run, in another terminal window: `python -m smtpd -n -c DebuggingServer localhost:1026`,
        - (or substitue your own settings for localhost:1026)
    """
    log.debug( f'settings.DEBUG, ``{settings.DEBUG}``' )
    if settings.DEBUG == True:
        log.debug( 'triggering exception' )
        raise Exception( 'Raising intentional exception.' )
    else:
        log.debug( 'returing 404' )
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )


def version( request ):
    """ Returns basic branch and commit data. """
    rq_now = datetime.datetime.now()
    gatherer = GatherCommitAndBranchData()
    trio.run( gatherer.manage_git_calls )
    commit = gatherer.commit
    branch = gatherer.branch
    info_txt = commit.replace( 'commit', branch )
    context = version_helper.make_context( request, rq_now, info_txt )
    output = json.dumps( context, sort_keys=True, indent=2 )
    log.debug( f'output, ``{output}``' )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def root( request ):
    return HttpResponseRedirect( reverse('info_url') )
