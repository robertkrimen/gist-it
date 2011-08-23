import re
import posixpath
import urlparse

def match( location ):
    return Gist.match( location )

def parse( location, **arguments ):
    return Gist.parse( location, **arguments )

def parse_slice( slice_ ):
    match = re.match( r'^(\d*):?(\d*)$', slice_ )
    if match is None:
        return ( 0, 0 )
    return map( lambda _: int(_) if len(_) else 0, match.groups(0) )

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

        return Gist( **parse )

    def __init__( self, **arguments ):
        for key in [ 'user', 'repository', 'branch', 'path',
                'blob_path', 'blob_url',
                'raw_path', 'raw_url', 
                'user_repository', 'user_repository_branch_path', 'user_repository_url' ]:
            setattr( self, key, arguments[ key ] )

