#!/usr/bin/env python
# vim: ft=python:
import random
import unittest2
import sys;
import os;

sys.path.append( os.path.join( sys.path[0], ".." ) )
import gist_it

class t( unittest2.TestCase ):
    def runTest( self ):
        self.assertEqual( gist_it.parse_highlight( 0 ), '0' )
        self.assertEqual( gist_it.parse_highlight( '0' ), '0' )
        self.assertEqual( gist_it.parse_highlight( False ), '0' )
        self.assertEqual( gist_it.parse_highlight( True ), 'prettify' )
        self.assertEqual( gist_it.parse_highlight( None ), 'prettify' )
        self.assertEqual( gist_it.parse_highlight( '  1' ), 'prettify' )
        self.assertEqual( gist_it.parse_highlight( 'yes  ' ), 'prettify' )
        self.assertEqual( gist_it.parse_highlight( '  no' ), '0' )
        self.assertEqual( gist_it.parse_highlight( 'none ' ), '0' )
        self.assertEqual( gist_it.parse_highlight( 'deferred-prettify' ), 'deferred-prettify' )

if __name__ == '__main__':
    unittest2.main()
