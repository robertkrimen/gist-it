#!/usr/bin/python
import logging
import os
import cgi
import sys
import urllib
import simplejson

jinja2 = None

_LOCAL_ = os.environ[ 'SERVER_SOFTWARE' ].startswith( 'Development' )
_DEBUG_ = True
_CACHE_ = False

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from versioned_memcache import memcache

import gist_it
from gist_it import take_slice, cgi_escape

def render_gist_html( base, gist, document ):
    if jinja2 is None:
        return
    result = jinja2.get_template( 'gist.jinja.html' ).render( cgi_escape = cgi_escape, base = base, gist = gist, document = document )
    return result

def render_gist_js( base, gist, gist_html  ):
    if jinja2 is None:
        return
    result = jinja2.get_template( 'gist.jinja.js' ).render( base = base, gist = gist, gist_html = gist_html )
    return result

def render_gist_js_callback( callback, gist, gist_html  ):
    return "%s( '%s', '%s' );" % ( callback, gist_html.encode( 'string_escape' ), gist.raw_path )

# dispatch == RequestHandler
def dispatch_test( dispatch ):
    dispatch.render_template( 'test.jinja.html', list =
        map( lambda _: ( _, 'github/robertkrimen/gist-it-example/raw/master/test.js?' + _ ), [
        # Standard
        ''
        # Without footer
        'footer=0',
        # Footer without "brought to you by" mention
        'footer=minimal',
        # Partial file
        'slice=3:10',
        # First line of file
        'slice=0',
        # Last line of file
        'slice=-1',
        # With no style request
        'style=0',
        # Documentation
        'slice=24:100',
        'slice=0:-2',
        'slice=0',
        ] )
    )

# dispatch == RequestHandler
def dispatch_test0( dispatch ):
    dispatch.render_template( 'test.jinja.html', list =
        map( lambda _: ( _, 'github/whittle/node-coffee-heroku-tutorial/raw/eb587185509ec8c2e728067d49f4ac2d5a67ec09/app.js?' + _ ), [
        # Standard
        ''
        ] )
    )

# dispatch == RequestHandler
def dispatch_gist_it( dispatch, location ):
    location = urllib.unquote( location )
    match = gist_it.Gist.match( location )
    dispatch.response.headers['Content-Type'] = 'text/plain'; 
    if not match:
        dispatch.response.set_status( 404 )
        dispatch.response.out.write( dispatch.response.http_status_message( 404 ) )
        dispatch.response.out.write( "\n" )
        return

    else:
        slice_option = dispatch.request.get( 'slice' )
        footer_option = dispatch.request.get( 'footer' )
        style_option = dispatch.request.get( 'style' )
        highlight_option = dispatch.request.get( 'highlight' )
        test = dispatch.request.get( 'test' )

        gist = gist_it.Gist.parse( location, slice_option = slice_option, footer_option = footer_option, style_option = style_option, highlight_option = highlight_option )
        if not gist:
            dispatch.response.set_status( 500 )
            dispatch.response.out.write( "Unable to parse \"%s\": Not a valid repository path?" % ( location ) )
            dispatch.response.out.write( "\n" )
            return
            
        if _CACHE_ and dispatch.request.get( 'flush' ):
            dispatch.response.out.write( memcache.delete( memcache_key ) )
            return

        memcache_key = gist.raw_url
        data = memcache.get( memcache_key )
        if data is None or not _CACHE_:
            base = dispatch.url_for()
            # For below, see: http://stackoverflow.com/questions/2826238/does-google-appengine-cache-external-requests
            response = urlfetch.fetch( gist.raw_url, headers = { 'Cache-Control': 'max-age=300' } )
            if response.status_code != 200:
                if response.status_code == 403:
                    dispatch.response.set_status( response.status_code )
                elif response.status_code == 404:
                    dispatch.response.set_status( response.status_code )
                else:
                    dispatch.response.set_status( 500 )
                dispatch.response.out.write( "Unable to fetch \"%s\": (%i)" % ( gist.raw_url, response.status_code ) )
                return
            else:
                # I believe GitHub always returns a utf-8 encoding, so this should be safe
                response_content = response.content.decode('utf-8')

                gist_content = take_slice( response_content, gist.start_line, gist.end_line )
                gist_html = str( render_gist_html( base, gist, gist_content ) ).strip()
                callback = dispatch.request.get( 'callback' );
                if callback != '':
                    result = render_gist_js_callback( callback, gist, gist_html )
                else:
                    result = render_gist_js( base, gist, gist_html )
                result = str( result ).strip()
                data = result
                if test:
                    if test == 'json':
                        dispatch.response.headers['Content-Type'] = 'application/json';
                        dispatch.response.out.write(simplejson.dumps({
                            'gist': gist.value(),
                            'content': gist_content,
                            'html': gist_html,
                        }))
                    elif False and test == 'example':
                        pass
                    else:
                        dispatch.response.headers['Content-Type'] = 'text/plain' 
                        dispatch.response.out.write( gist_html )
                    return
                if _CACHE_:
                    memcache.add( memcache_key, data, 60 * 60 * 24 )

        dispatch.response.headers['Content-Type'] = 'text/javascript'
        dispatch.response.out.write( data )
