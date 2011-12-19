#!/usr/bin/env perl

use strict;
use warnings;

use lib 't/p5/lib/perl5';
use local::lib 't/p5';

use Test::Most;
use Test::HTTP;

my $base = "http://localhost:8080"; 
my $is_local = $base =~ m/localhost/;
diag "\$base = $base";
my $test = Test::HTTP->new( '' );

my ( $body, $body_re );

$test->get( "$base" );
$test->status_code_is( 200 );
$test->body_like( qr/Description/ );
$test->body_like( qr/Usage/ );

$test->get( "$base/github/robertkrimen/gist-it-example/blob/master/README" );
$test->status_code_is( 200 );

$test->get( "$base/github.com/robertkrimen/gist-it-example/blob/master/README" );
$test->status_code_is( 200 );

$test->get( "$base/github/robertkrimen/gist-it-example/blob/master/example.js" );
$test->status_code_is( 200 );

$test->body_like( qr/\Qif ( 'prettyPrint' in window ) {} else {\E/ );
$test->body_like( qr{\Qdocument.write( '<script type="text/javascript" src="$base/assets/prettify/prettify.js"></script>' )\E} );
$test->body_like( qr{\Qdocument.write( '<link rel="stylesheet" href="$base/assets/embed.css"/>' )\E} );
$test->body_like( qr{\Qdocument.write( '<link rel="stylesheet" href="$base/assets/prettify/prettify.css"/>' )\E} );
$test->body_like( qr{\Qdocument.write( '<script type="text/javascript">prettyPrint();</script>' )\E} );
$test->body_like( qr{\Q<div class="gister-gist">\E} );
$test->body_like( qr{\Q<div class="gist-file">\E} );
$test->body_like( qr{\Q<div class="gist-data">\E} );
$test->body_like( qr!\Q<pre class="prettyprint">function Xyzzy() {\n    return "Nothing happens";\n}\n</pre>\E! );
$test->body_like( qr{\Q<div class="gist-meta">\E} );
$test->body_like( qr{\Q<span><a href="https://github.com/robertkrimen/gist-it-example/blob/master/example.js">This Gist</a> brought to you by <a href="$base">gist-it</a>.</span>\E} );
$test->body_like( qr{\Q<span style="float: right; color: #369;"><a href="https://github.com/robertkrimen/gist-it-example/raw/master/example.js">view raw</a></span>\E} );
$test->body_like( qr{\Q<span style="float: right; margin-right: 8px;">\E\s*\\n\s*\Q<a style="color: rgb(102, 102, 102);" href="https://github.com/robertkrimen/gist-it-example/blob/master/example.js">example.js</a></span\E} );

my @resource = $test->_decoded_content =~ m{(?:script type="text/javascript" src|link rel="stylesheet" href)="([^"]+)"}g;
is( scalar @resource, 3 );
SKIP: {
    skip 'local', 3 if $is_local;
    for my $resource ( @resource ) {
        unlike( $resource, qr/localhost/, "$resource is not a localhost resource" );
        $test->get( "$resource" );
        $test->status_code_is( 200, "GET $resource" );
    }
}

$test->get( "$base/github/robertkrimen/as3-projection/blob/master/src/yzzy/projection/Aperture.as" );
$test->body_like( qr/yzzy\.projection/ );
$test->status_code_is( 200 );

$test->get( "$base/github/miyagawa/CPAN-Any/blob/master/README" );
$test->status_code_is( 200 );
$test->body_like( qr/CPAN::Any/ );

$test->get( "$base/github/robertkrimen" );
$test->status_code_is( 500 );
$test->body_like( qr{\QUnable to parse "/github/robertkrimen": Not a valid repository path?\E} );

$test->get( "$base/github/robertkrimen/gist-it-example" );
$test->status_code_is( 500 );
$test->body_like( qr{\QUnable to parse "/github/robertkrimen/gist-it-example": Not a valid repository path?\E} );

$test->get( "$base/github/robertkrimen/gist-it-example/blob" );
$test->status_code_is( 500 );
$test->body_like( qr{\QUnable to parse "/github/robertkrimen/gist-it-example/blob": Not a valid repository path?\E} );

$test->get( "$base/github/robertkrimen/gist-it-example/blob/master" );
$test->status_code_is( 500 );
$test->body_like( qr{\QUnable to parse "/github/robertkrimen/gist-it-example/blob/master": Not a valid repository path?\E} );

$test->get( "$base/github/robertkrimen/gist-it-example/blob/master/" );
$test->status_code_is( 500 );
$test->body_like( qr{\QUnable to parse "/github/robertkrimen/gist-it-example/blob/master/": Not a valid repository path?\E} );

$test->get( "$base/github/robertkrimen/gist-it-example/blob/master/Test" );
$test->status_code_is( 404 );
$test->body_like( qr{\QUnable to fetch "https://github.com/robertkrimen/gist-it-example/raw/master/Test": (404)\E} );

$test->get( "$base/github/robertkrimen/gist-it-example/master/blob/README" );
diag( $body = $test->_decoded_content );
$test->status_code_is( 404 );
$test->body_like( qr{\QUnable to fetch "https://github.com/robertkrimen/gist-it-example/raw/blob/README": (404)\E} );

$test->get( "$base/github" );
$test->status_code_is( 404 );
$test->body_like( qr{\QNot Found\E} );

$test->get( "$base/xyzzy" );
$test->status_code_is( 404 );
$test->body_like( qr{\QNot Found\E} );

$test->get( "$base/github/" );
$test->status_code_is( 500 );
$test->body_like( qr{\QUnable to parse "/github/": Not a valid repository path?\E} );
diag $test->response->decoded_content;

for (qw[
    embed.css
    prettify/prettify.css
    prettify/prettify.js
]){
    $test->get( "$base/assets/$_" );
    $test->status_code_is( 200, $_ );
}

$test->get( "$base/xyzzy/github/robertkrimen/gist-it-example/blob/master" );
$test->status_code_is( 500 );
$test->body_like( qr{\QUnable to parse "github/robertkrimen/gist-it-example/blob/master": Not a valid repository path?\E} );

$test->get( "$base/xyzzy/github/miyagawa/CPAN-Any/blob/master/README" );
$test->status_code_is( 200 );
$test->body_like( qr/CPAN::Any/ );

done_testing;
