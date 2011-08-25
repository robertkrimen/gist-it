#!/usr/bin/python
import logging
import new
import os
import pickle
import cgi
import sys
import traceback
import urlparse
import types
import wsgiref.handlers
import re
import posixpath
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

_LOCAL_ = os.environ[ 'SERVER_SOFTWARE' ].startswith( 'Development' )
_DEBUG_ = False or _LOCAL_
_CACHE_ = False

sys.path.append( 'pyl' )

import jinja2 as jinja2_
jinja2 = jinja2_.Environment( loader=jinja2_.FileSystemLoader( 'jinja2-assets' ) )

from gist_it import appengine as gist_it_appengine
gist_it_appengine.jinja2 = jinja2

class RequestHandler( webapp.RequestHandler ):

    def url_for( self, *arguments ):
        parse = urlparse.urlparse( self.request.url )
        path = ''
        if len( arguments ):
            path = posixpath.join( *arguments )
        return str( urlparse.urlunparse( ( parse.scheme, parse.netloc, path, '', '', '' ) ) )

    def render_template( self, template_name, **arguments ):
        self.response.out.write( jinja2.get_template( template_name ).render( dispatch=self, **arguments ) )

class dispatch_index( RequestHandler ):
    def get( self ):
        self.render_template( 'index.jinja.html' )

class dispatch_gist_it( RequestHandler ):
    def get( self, location ):
        return gist_it_appengine.dispatch_gist_it( self, location )

wsgi_application = webapp.WSGIApplication( [
    ( r'/', dispatch_index ),
    ( r'/xyzzy/(.*)', dispatch_gist_it ),
    ( r'(.*)', dispatch_gist_it ),
], debug=_DEBUG_ )

def main():
    run_wsgi_app( wsgi_application )

if __name__ == '__main__':
    main()
