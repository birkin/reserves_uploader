import logging

log = logging.getLogger(__name__)


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