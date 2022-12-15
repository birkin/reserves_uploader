import json, logging

from django.conf import settings as project_settings
from django.test import SimpleTestCase as TestCase  # `from django.test import TestCase` requires db
from django.test.utils import override_settings
from reserves_uploader_app.lib import pather


log = logging.getLogger(__name__)
TestCase.maxDiff = 1000


class PathsTest( TestCase ):
    """ Checks paths. """

    def test_paths(self):
        """ Checks paths. """
        root_path = '/path/to/files'
        self.assertEqual(
            '/path/to/files/12/34/1234567890.pdf',
            pather.create_file_path( '1234567890.pdf', root_path ) 
        )

    def test_paths_multiple(self):
        """ Checks paths in bulk. 
            TODO: add a challenging unicode-normalization entry. """
        root_path = '/path/to/files'
        file_names = [ 
            '1234567890.pdf', 
            'iñtërnâtiônàlĭzætiøn.pdf', 
            '.abcdef.txt', 
            ' qabcdef.txt',
            '. bcdef.txt',
            'cde.txt',
            'de.txt',
            'f.txt',
            'gh ij kl.txt',
        ]
        expected = [
            '/path/to/files/12/34/1234567890.pdf',
            '/path/to/files/iñ/të/iñtërnâtiônàlĭzætiøn.pdf',
            '/path/to/files/ab/cd/abcdef.txt',
            '/path/to/files/qa/bc/qabcdef.txt',
            '/path/to/files/bc/de/bcdef.txt',
            'z/path/to/files/cd/cde.txt',
            'zz/path/to/files/de.txt',
            'zzz/path/to/files/f.txt',
            'zzzz/path/to/files/gh/_i/gh_ij_kl.txt'
        ]
        for i, file_name in enumerate(file_names):
            self.assertEqual( expected[i], pather.create_file_path( file_name, root_path )    
        )


class ErrorCheckTest( TestCase ):
    """ Checks urls. """

    @override_settings(DEBUG=True)  # for tests, DEBUG autosets to False
    def test_dev_errorcheck(self):
        """ Checks that dev error_check url triggers error.. """
        log.debug( f'debug, ``{project_settings.DEBUG}``' )
        try:
            log.debug( 'about to initiate client.get()' )
            response = self.client.get( '/error_check/' )
        except Exception as e:
            log.debug( f'e, ``{repr(e)}``' )
            self.assertEqual( "Exception('Raising intentional exception.')", repr(e) )

    def test_prod_errorcheck(self):
        """ Checks that production error_check url returns 404. """
        log.debug( f'debug, ``{project_settings.DEBUG}``' )
        response = self.client.get( '/error_check/' )
        self.assertEqual( 404, response.status_code )
