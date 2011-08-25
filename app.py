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

from versioned_memcache import memcache

import jinja2 as jinja2_
jinja2 = jinja2_.Environment( loader=jinja2_.FileSystemLoader( 'jinja2-assets' ) )

import gist_it
from gist_it import take_slice

def render_gist_html( base, gist, document ):
    result = jinja2.get_template( 'gist.jinja.html' ).render( cgi = cgi, base = base, gist = gist, document = document )
    return result

def render_gist_js( base, gist, gist_html  ):
    result = jinja2.get_template( 'gist.jinja.js' ).render( base = base, gist = gist, gist_html = gist_html )
    return result

def render_gist_js_callback( callback, gist, gist_html  ):
    return "%s( '%s', '%s' );" % ( callback, gist_html.encode( 'string_escape' ), gist.raw_path )

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
        base = self.url_for()
        location = urllib.unquote( location )
        match = gist_it.Gist.match( location )
        self.response.headers['Content-Type'] = 'text/plain'; 
        if not match:
            self.response.set_status( 404 )
            self.response.out.write( self.response.http_status_message( 404 ) )
            self.response.out.write( "\n" )
            return

        else:
            gist = gist_it.Gist.parse( location, slice_ = self.request.get( 'slice' ) )
            if not gist:
                self.response.set_status( 500 )
                self.response.out.write( "Unable to parse \"%s\": Not a valid repository path?" % ( location ) )
                self.response.out.write( "\n" )
                return
                
            if _CACHE_ and self.request.get( 'flush' ):
                self.response.out.write( memcache.delete( memcache_key ) )
                return

            memcache_key = gist.raw_url
            data = memcache.get( memcache_key )
            if data is None or not _CACHE_:
                # For below, see: http://stackoverflow.com/questions/2826238/does-google-appengine-cache-external-requests
                response = urlfetch.fetch( gist.raw_url, headers = { 'Cache-Control': 'max-age=300' } )
                if response.status_code != 200:
                    if response.status_code == 403:
                        self.response.set_status( response.status_code )
                    elif response.status_code == 404:
                        self.response.set_status( response.status_code )
                    else:
                        self.response.set_status( 500 )
                    self.response.out.write( "Unable to fetch \"%s\": (%i)" % ( gist.raw_url, response.status_code ) )
                    return
                else:
                    gist_content = take_slice( response.content, gist.start_line, gist.end_line )
                    if self.request.get( 'test' ):
                        self.response.headers['Content-Type'] = 'text/plain'; 
                        self.response.out.write( gist_content )
                        return
                    else:
                        gist_html = str( render_gist_html( base, gist, gist_content ) ).strip()
                        callback = self.request.get( 'callback' );
                        if callback != '':
                            result = render_gist_js_callback( callback, gist, gist_html )
                        else:
                            result = render_gist_js( base, gist, gist_html )
                        result = str( result ).strip()
                        data = result
                        if _CACHE_:
                            memcache.add( memcache_key, data, 60 * 60 * 24 )

            self.response.headers['Content-Type'] = 'text/javascript'; 
            self.response.out.write( data )

wsgi_application = webapp.WSGIApplication( [
    ( r'/', dispatch_index ),
    ( r'/xyzzy/(.*)', dispatch_gist_it ),
    ( r'(.*)', dispatch_gist_it ),
], debug=_DEBUG_ )

def main():
    run_wsgi_app( wsgi_application )

if __name__ == '__main__':
    main()
