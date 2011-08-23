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
        slice_ = gist_it.parse_slice( '' )
        self.assertEqual( len( slice_ ), 2 )
        self.assertEqual( slice_[0], 0 )
        self.assertEqual( slice_[1], 0 )

        slice_ = gist_it.parse_slice( '1' )
        self.assertEqual( len( slice_ ), 2 )
        self.assertEqual( slice_[0], 1 )
        self.assertEqual( slice_[1], 0 )

        slice_ = gist_it.parse_slice( '1:' )
        self.assertEqual( len( slice_ ), 2 )
        self.assertEqual( slice_[0], 1 )
        self.assertEqual( slice_[1], 0 )

        slice_ = gist_it.parse_slice( '1:0' )
        self.assertEqual( len( slice_ ), 2 )
        self.assertEqual( slice_[0], 1 )
        self.assertEqual( slice_[1], 0 )

        slice_ = gist_it.parse_slice( ':1' )
        self.assertEqual( len( slice_ ), 2 )
        self.assertEqual( slice_[0], 0 )
        self.assertEqual( slice_[1], 1 )

        slice_ = gist_it.parse_slice( '0:1' )
        self.assertEqual( len( slice_ ), 2 )
        self.assertEqual( slice_[0], 0 )
        self.assertEqual( slice_[1], 1 )

        slice_ = gist_it.parse_slice( '1:1' )
        self.assertEqual( len( slice_ ), 2 )
        self.assertEqual( slice_[0], 1 )
        self.assertEqual( slice_[1], 1 )

        slice_ = gist_it.parse_slice( ':' )
        self.assertEqual( len( slice_ ), 2 )
        self.assertEqual( slice_[0], 0 )
        self.assertEqual( slice_[1], 0 )

if __name__ == '__main__':
    unittest2.main()
