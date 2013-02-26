import re
import posixpath
import urlparse
import cgi

def cgi_escape( content ):
    return cgi.escape(content).encode('ascii', 'xmlcharrefreplace')

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
    elif footer_option == 'minimal':
        return footer_option
    else:
        return '1'

def parse_style( style_option ):
    if style_option is None or style_option is True:
        return '1'
    elif style_option is False:
        return '0'

    style_option = str( style_option ).lower().strip()
    if style_option == '1' or style_option == '' or style_option == 'true':
        return '1'
    elif style_option == '0' or style_option == 'false' or style_option == 'none' or style_option == 'no':
        return '0'
    else:
        return '1'

def parse_highlight( option ):
    if option is None or option is True:
        return 'prettify'
    elif option is False:
        return '0'

    option = str( option ).lower().strip()
    if option == '1' or option == '' or option == 'true':
        return 'prettify'
    elif option == '0' or option == 'false' or option == 'none' or option == 'no':
        return '0'
    elif option == 'deferred-prettify':
        return option
    else:
        return 'prettify'

def parse_slice( slice_option ):
    if slice_option is None:
        return ( 0, 0 )
    
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

    if (end_line > 0):
        end_line += 1

    return '\n'.join(content.splitlines()[start_line:end_line])

class Gist:

    @classmethod
    def keylist( self ):
        return [
            'user', 'repository', 'branch', 'path',
            'blob_path', 'blob_url',
            'raw_path', 'raw_url', 
            'user_repository', 'user_repository_branch_path', 'user_repository_url',
            'start_line', 'end_line',
            'footer', 'style', 'highlight',
            'filename',
        ]

    @classmethod
    def match( self, location ):
        match = re.match( r'^(?:/https?:/)?/?github(?:\.com)?/(.*)$', location )
        if not match:
            return None
        return match

    @classmethod
    def parse( self, location, slice_option = None, footer_option = None, style_option = None, highlight_option = None ):
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

        slice_option = parse_slice( slice_option )
        parse[ 'start_line' ] = slice_option[0]
        parse[ 'end_line' ] = slice_option[1]

        parse[ 'footer' ] = parse_footer( footer_option )
        parse[ 'style' ] = parse_style( style_option )
        parse[ 'highlight' ] = parse_highlight( highlight_option )

        parse[ 'filename' ] = splitpath[-1]

        return Gist( **parse )

    def __init__( self, **arguments ):
        for key in self.keylist():
            setattr( self, key, arguments[ key ] )

    def value( self ):
        value = {}
        for key in self.keylist():
            value[ key ] = getattr( self, key )
        return value
