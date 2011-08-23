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
        self.assertTrue( True, 'Xyzzy' )

        self.assertTrue( gist_it.match( 'github/robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' ) )

        gist = gist_it.parse( 'github/robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' )
        self.assertEqual( gist.user, 'robertkrimen' )
        self.assertEqual( gist.repository, 'yzzy-projection' )
        self.assertEqual( gist.branch, 'master' )
        self.assertEqual( gist.path, 'src/yzzy/projection/View.as' )

        self.assertEqual( gist.blob_path, 'robertkrimen/yzzy-projection/blob/master/src/yzzy/projection/View.as' )
        self.assertEqual( gist.blob_url, 'https://github.com/robertkrimen/yzzy-projection/blob/master/src/yzzy/projection/View.as' )

        self.assertEqual( gist.raw_path, 'robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' )
        self.assertEqual( gist.raw_url, 'https://github.com/robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' )

        self.assertEqual( gist.user_repository, 'robertkrimen/yzzy-projection' )
        self.assertEqual( gist.user_repository_branch_path, 'robertkrimen/yzzy-projection/master/src/yzzy/projection/View.as' )
        self.assertEqual( gist.user_repository_url, 'https://github.com/robertkrimen/yzzy-projection' )

        self.assertEqual( gist.start_line, 0 )
        self.assertEqual( gist.end_line, 0 )

        gist = gist_it.parse( 'github/robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as', slice_ = '1:' )

        self.assertEqual( gist.start_line, 1 )
        self.assertEqual( gist.end_line, 0 )

if __name__ == '__main__':
    unittest2.main()
