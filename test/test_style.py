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
        self.assertEqual( gist_it.parse_style( 0 ), '0' )
        self.assertEqual( gist_it.parse_style( '0' ), '0' )
        self.assertEqual( gist_it.parse_style( False ), '0' )
        self.assertEqual( gist_it.parse_style( True ), '1' )
        self.assertEqual( gist_it.parse_style( None ), '1' )
        self.assertEqual( gist_it.parse_style( '  1' ), '1' )
        self.assertEqual( gist_it.parse_style( 'yes  ' ), '1' )
        self.assertEqual( gist_it.parse_style( '  no' ), '0' )
        self.assertEqual( gist_it.parse_style( 'none ' ), '0' )

if __name__ == '__main__':
    unittest2.main()
