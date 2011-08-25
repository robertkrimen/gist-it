import re
import posixpath
import urlparse

def match( location ):
    return Gist.match( location )

def parse( location, **arguments ):
    return Gist.parse( location, **arguments )

def parse_footer( footer_option ):
    if footer_option is None or footer_option is True:
        return '1'
    elif footer_option is False:
        return '0'

    footer_option = str( footer_option ).lower().strip()
    if footer_option == '1' or footer_option == '' or footer_option == 'true':
        return '1'
    elif footer_option == '0' or footer_option == 'false' or footer_option == 'none' or footer_option == 'no':
        return '0'
    elif footer_option == 'noby':
        return footer_option
    else:
        return '1'

def parse_slice( slice_option ):
    match = re.match( r'^(-?\d+)$', slice_option )
    if match:
        return ( int( match.group(1) ), None )

    match = re.match( r'^(-?\d+)?:?(-?\d+)?$', slice_option )
    if match is None:
        return ( 0, 0 )

    return map( lambda _: int(_) if _ is not None else 0, match.groups() )

'''
Take a (line) slice of content, based on a start/end index
'''
def take_slice( content, start_line = None, end_line = None ):
    if (start_line is None and end_line is None):
        return content

    if (start_line == 0 and end_line == 0):
        return content
    
    if (end_line == 0):
        return '\n'.join(content.splitlines()[start_line:])

    if (end_line is None):
        return content.splitlines()[start_line]

    return '\n'.join(content.splitlines()[start_line:end_line])

class Gist:

    @classmethod
    def match( self, location ):
        match = re.match( r'^(?:/https?:/)?/?github(?:\.com)?/(.*)$', location )
        if not match:
            return None
        return match

    @classmethod
    def parse( self, location, slice_ = '' ):
        match = self.match( location )
        if not match:
            return None

        path = match.group( 1 )
        splitpath = posixpath.normpath( path ).split( '/' )
        if len( splitpath ) < 5:
            return None

        parse = {}

        # user / respository / format / branch / path
        user        = parse[ 'user' ]       = splitpath[ 0 ]
        repository  = parse[ 'repository' ] = splitpath[ 1 ]
        branch      = parse[ 'branch' ]     = splitpath[ 3 ]
        path        = parse[ 'path' ]       = '/'.join( splitpath[ 4: ] )

        # format = blob
        splitpath[ 2 ] = 'blob'
        blob_path   = parse[ 'blob_path' ]  = '/'.join( splitpath )
        blob_url    = parse[ 'blob_url' ]   = urlparse.urljoin( 'https://github.com', blob_path )

        # format = raw
        splitpath[ 2 ] = 'raw'
        raw_path    = parse[ 'raw_path' ]   = '/'.join( splitpath )
        raw_url     = parse[ 'raw_url' ]    = urlparse.urljoin( 'https://github.com', raw_path )

        user_repository             = parse[ 'user_repository' ]                = '/'.join([ user, repository ])
        user_repository_branch_path = parse[ 'user_repository_branch_path' ]    = '/'.join([ user_repository, branch, path ]);
        user_repository_url         = parse[ 'user_repository_url' ]            = urlparse.urljoin( 'https://github.com', user_repository )

        slice_ = parse_slice( slice_ )
        parse[ 'start_line' ] = slice_[0]
        parse[ 'end_line' ] = slice_[1]

        return Gist( **parse )

    def __init__( self, **arguments ):
        for key in [ 'user', 'repository', 'branch', 'path',
                'blob_path', 'blob_url',
                'raw_path', 'raw_url', 
                'user_repository', 'user_repository_branch_path', 'user_repository_url',
                'start_line', 'end_line',
                ]:
            setattr( self, key, arguments[ key ] )

