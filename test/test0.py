#!/usr/bin/env python
# vim: ft=python:
import random
import unittest2
import sys;
import os;

sys.path.append( os.path.join( sys.path[0], ".." ) )
import util

class t( unittest2.TestCase ):
    def runTest( self ):
        self.assertTrue( True, 'Xyzzy' )

        parse = util.parse_github_path( 'robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' )
        self.assertEqual( parse['blob-path'], 'robertkrimen/yzzy-projection/blob/master/src/yzzy/projection/View.as' )
        self.assertEqual( parse['raw-url'], 'https://github.com/robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' )
        self.assertEqual( parse['path'], 'src/yzzy/projection/View.as' )
        self.assertEqual( parse['user-repository-branch-path'], 'robertkrimen/yzzy-projection/master/src/yzzy/projection/View.as' )
        self.assertEqual( parse['user-repository'], 'robertkrimen/yzzy-projection' )

        gist = util.Gist.parse( 'robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' )
        self.assertEqual( gist.user, 'robertkrimen' )

if __name__ == '__main__':
    unittest2.main()
