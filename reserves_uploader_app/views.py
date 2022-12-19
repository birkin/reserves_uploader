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

# def uploader( request ):
#     """ On GET, return the uploader page.
#         On POST, process the uploaded file via django chunked-upload. """
#     log.debug( 'starting' )
#     if request.method == 'POST':
#         log.debug( 'request.POST, ``%s``' % request.POST )
#         log.debug( 'request.FILES, ``%s``' % request.FILES )
#         return HttpResponse( 'Thanks for the upload!' )
#     else:
#         return render( request, 'reserves_uploader_app/uploader.html' )


def info(request):
    return HttpResponse( "zHello, world." )


@ensure_csrf_cookie
def uploader(request):
    log.debug( 'starting uploader()' )
    # log.debug( f'inital incoming request.session.items(), ``{pprint.pformat(request.session.items())}``' )
    if request.method == 'POST':
        log.debug( 'POST detected' )
        log.debug( f'request.POST, ``{pprint.pformat(request.POST)}``' )
        log.debug( f'request.FILES, ``{pprint.pformat(request.FILES)}``' )
        log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
        assert request.session['msg'] == ''
        log.debug( 'about to instantiate form' )

        form = UploadFileForm(request.POST, request.FILES)
        log.debug( f'form.__dict__, ``{pprint.pformat(form.__dict__)}``' )
        if form.is_valid():
            log.debug( 'form is valid' )
            log.debug( f'form.cleaned_data, ``{pprint.pformat(form.cleaned_data)}``' )
            # log.debug( f'form.cleaned_data.__dict__, ``{pprint.pformat(form.cleaned_data.__dict__)}``' )
            # log.debug( f'form.cleaned_data["file"], ``{pprint.pformat(form.cleaned_data["file"])}``' )
            # log.debug( f'form.cleaned_data["file"].name, ``{pprint.pformat(form.cleaned_data["file"].name)}``' )
            handle_uploaded_file( request.FILES['file'] )
            # context = {'msg' : '<span style="color: green;">File successfully uploaded</span>'}
            msg = 'File successfully uploaded'
            request.session['msg'] = msg
            log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
            # return render(request, 'templates/single_file.html', context)
        else:
            log.debug( 'form not valid' )
            log.debug( f'form.errors, ``{pprint.pformat(form.errors)}``' )
            log.debug( f'form.non_field_errors(), ``{pprint.pformat(form.non_field_errors())}``' )
            error_message = form.non_field_errors()[0]
            log.debug( f'error_message, ``{pprint.pformat(error_message)}``' )
            # context = {'msg' : '<span style="color: red;">Form not valid</span>'}
            # resp = render(request, 'templates/single_file.html', context)
            # msg = f'<span style="color: red;">Form not valid, error: {error_message}</span>'
            # msg = f'Form not valid, error: ``{error_message}``.'
            # request.session['msg'] = msg
            request.session['msg'] = error_message
        log.debug( 'POST handled, about to redirect' )
        log.debug( f'at end of POST; request.session.keys(), ``{pprint.pformat(request.session.keys())}``' )
        log.debug( f'at end of POST; request.session["msg"], ``{pprint.pformat(request.session["msg"])}``' )
        resp = HttpResponseRedirect( reverse('uploader_url') )  ## TODO, add message as querystring, then display it
    elif request.method == 'GET':
        log.debug( 'GET detected' )
        log.debug( f'request.session.items(), ``{pprint.pformat(request.session.items())}``' )
        ## get any session message ----------------------------------
        session_message = request.session.get('msg', '')
        log.debug( f'session_message, ``{session_message}``' )
        ## clear out session message --------------------------------
        request.session['msg'] = ''
        # form = UploadFileForm()
        context: dict = uploader_helper.build_uploader_GET_context( session_message )
        # resp = render( request, 'templates/single_file.html', {'form': form} )
        # resp = render( request, 'single_file.html', {'form': form} )
        resp = render( request, 'single_file.html', context )
    else:
        resp = HttpResponseBadRequest( 'bad request' )
    return resp



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

# def handle_uploaded_file(f):
#     """ Handles uploaded file.
#         Currently overwrites existing file."""
#     log.debug( f'f.__dict__, ``{pprint.pformat(f.__dict__)}``' )
#     full_file_path = f'{settings.UPLOADS_DIR_PATH}/{f.name}'
#     with open( full_file_path, 'wb+' ) as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#     log.debug( f'writing finished' )
#     return




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
