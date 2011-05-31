import re
import posixpath
import urlparse

class Gist:

    @classmethod
    def match( self, location ):
        match = re.match( r'^(?:/https?:/)?/?github(?:\.com)?/(.*)$', location )
        if not match:
            return None
        return match

    @classmethod
    def parse( self, location ):
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

def parse_github_path( path ):
    splitpath = posixpath.normpath( path ).split( '/' )
    parse = {}

    if len( splitpath ) < 5:
        return None

    # '(user)/(repository)/(format)/(path)'
    user = parse['user'] = splitpath[ 0 ]
    repository = parse['repository'] = splitpath[ 1 ]
    branch = parse['branch'] = splitpath[ 3 ]
    path = parse['path'] = '/'.join( splitpath[ 4: ] )

    splitpath[ 2 ] = 'blob'
    _path = parse['blob-path'] = '/'.join( splitpath )
    parse['blob-url'] = urlparse.urljoin( 'https://github.com', _path )

    splitpath[ 2 ] = 'raw'
    _path = parse['raw-path'] = '/'.join( splitpath )
    parse['raw-url'] = urlparse.urljoin( 'https://github.com', _path )

    parse['user-repository-branch-path'] = '/'.join([ user, repository, branch, path ]);
    parse['user-repository'] = '/'.join([ user, repository ])
    parse['user-repository-url'] = urlparse.urljoin( 'https://github.com', parse['user-repository'] )

    return parse
