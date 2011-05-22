import re
import posixpath
import urlparse

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
