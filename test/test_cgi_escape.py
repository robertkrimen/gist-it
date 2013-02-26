#!/usr/bin/env python
# vim: ft=python: set fileencoding=utf-8
import random
import unittest2
import sys;
import os;

sys.path.append( os.path.join( sys.path[0], ".." ) )
from gist_it import cgi_escape

# https://github.com/whittle/node-coffee-heroku-tutorial/blob/eb587185509ec8c2e728067d49f4ac2d5a67ec09/app.js
class t( unittest2.TestCase ):
    def runTest( self ):
        self.assertEqual( len(cgi_escape( """
(function() {
  var http = require('http');

  var say_nothing = function(request, response) {
    var message = 'مرحبا العالم';

    response.setHeader('Content-Type', 'text/plain; charset=utf-8');
    response.setHeader('X-Bad-Content-Length', message.length);
    response.setHeader('Content-Length', Buffer.byteLength(message, 'utf8'));
    response.write(message, 'utf8');
    response.end();
  };

  var app = http.createServer(say_nothing);
  app.listen(3080);
})();

""".decode('utf-8') ) ), 542 )

if __name__ == '__main__':
    unittest2.main()
