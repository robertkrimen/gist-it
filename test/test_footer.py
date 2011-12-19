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
        self.assertEqual( gist_it.parse_footer( 0 ), '0' )
        self.assertEqual( gist_it.parse_footer( '0' ), '0' )
        self.assertEqual( gist_it.parse_footer( False ), '0' )
        self.assertEqual( gist_it.parse_footer( True ), '1' )
        self.assertEqual( gist_it.parse_footer( None ), '1' )
        self.assertEqual( gist_it.parse_footer( '  1' ), '1' )
        self.assertEqual( gist_it.parse_footer( 'yes  ' ), '1' )
        self.assertEqual( gist_it.parse_footer( '  no' ), '0' )
        self.assertEqual( gist_it.parse_footer( 'none ' ), '0' )
        self.assertEqual( gist_it.parse_footer( ' minimal ' ), 'minimal' )

if __name__ == '__main__':
    unittest2.main()
