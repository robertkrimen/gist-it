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

        self.assertTrue( util.Gist.match( 'github/robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' ) )

        gist = util.Gist.parse( 'github/robertkrimen/yzzy-projection/raw/master/src/yzzy/projection/View.as' )
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

if __name__ == '__main__':
    unittest2.main()
