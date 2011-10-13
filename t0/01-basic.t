#!/usr/bin/env perl

use strict;
use warnings;

use Test::Most;
use Test::HTTP::TWIM;

my $base = "http://localhost:8080"; 
my $is_local = $base =~ m/localhost/;
diag "\$base = $base";

my $twim = Test::HTTP::TWIM->twim( base => $base );

my ( $body, $body_re );

$twim->get( '/' );
$twim->status_code_is( 200 );
$twim->body_like( qr/Description/ );
$twim->body_like( qr/Usage/ );

$twim->get( "/github/robertkrimen/gist-it-example/blob/master/README" );
$twim->status_code_is( 200 );

$twim->get( "/github.com/robertkrimen/gist-it-example/blob/master/README" );
$twim->status_code_is( 200 );

$twim->get( "/github/robertkrimen/gist-it-example/blob/master/example.js" );
$twim->status_code_is( 200 );

$twim->body_like( qr/\Qif ( 'prettyPrint' in window ) {} else {\E/ );
$twim->body_like( qr{\Qdocument.write( '<script type="text/javascript" src="$base/assets/prettify/prettify.js"></script>' )\E} );
$twim->body_like( qr{\Qdocument.write( '<link rel="stylesheet" href="$base/assets/embed.css"/>' )\E} );
$twim->body_like( qr{\Qdocument.write( '<link rel="stylesheet" href="$base/assets/prettify/prettify.css"/>' )\E} );
$twim->body_like( qr{\Qdocument.write( '<script type="text/javascript">prettyPrint();</script>' )\E} );
$twim->body_like( qr{\Q<div class="gister-gist">\E} );
$twim->body_like( qr{\Q<div class="gist-file">\E} );
$twim->body_like( qr{\Q<div class="gist-data">\E} );
$twim->body_like( qr!\Q<pre class="prettyprint">function Xyzzy() {\n    return "Nothing happens";\n}\n</pre>\E! );
$twim->body_like( qr{\Q<div class="gist-meta">\E} );
$twim->body_like( qr{\Q<span><a href="https://github.com/robertkrimen/gist-it-example/blob/master/example.js">This Gist</a> by <a href="$base">gist-it</a></span>\E} );
$twim->body_like( qr{\Q<span style="float: right; color: #369;"><a href="https://github.com/robertkrimen/gist-it-example/raw/master/example.js">view raw</a></span>\E} );
$twim->body_like( qr{\Q<span style="float: right; margin-right: 8px;">\E\s*\\n\s*\Q<a style="color: rgb(102, 102, 102);" href="https://github.com/robertkrimen/gist-it-example/blob/master/example.js">example.js</a></span\E} );

my @resource = $twim->response->body =~ m{(?:script type="text/javascript" src|link rel="stylesheet" href)="([^"]+)"}g;
is( scalar @resource, 3 );
SKIP: {
    skip 'local', 3 if $is_local;
    for my $resource ( @resource ) {
        unlike( $resource, qr/localhost/, "$resource is not a localhost resource" );
        $twim->get( "$resource" );
        $twim->status_code_is( 200, "GET $resource" );
    }
}

$twim->get( "github/robertkrimen/as3-projection/blob/master/src/yzzy/projection/Aperture.as" );
$twim->body_like( qr/yzzy\.projection/ );
$twim->status_code_is( 200 );

$twim->get( "github/miyagawa/CPAN-Any/blob/master/README" );
$twim->status_code_is( 200 );
$twim->body_like( qr/CPAN::Any/ );

$twim->get_fail( "github/robertkrimen" );
$twim->status_code_is( 500 );
$twim->body_like( qr{\QUnable to parse "/github/robertkrimen": Not a valid repository path?\E} );

$twim->get_fail( "github/robertkrimen/gist-it-example" );
$twim->status_code_is( 500 );
$twim->body_like( qr{\QUnable to parse "/github/robertkrimen/gist-it-example": Not a valid repository path?\E} );

$twim->get_fail( "github/robertkrimen/gist-it-example/blob" );
$twim->status_code_is( 500 );
$twim->body_like( qr{\QUnable to parse "/github/robertkrimen/gist-it-example/blob": Not a valid repository path?\E} );

$twim->get_fail( "github/robertkrimen/gist-it-example/blob/master" );
$twim->status_code_is( 500 );
$twim->body_like( qr{\QUnable to parse "/github/robertkrimen/gist-it-example/blob/master": Not a valid repository path?\E} );

$twim->get_fail( "github/robertkrimen/gist-it-example/blob/master/" );
$twim->status_code_is( 500 );
$twim->body_like( qr{\QUnable to parse "/github/robertkrimen/gist-it-example/blob/master/": Not a valid repository path?\E} );

$twim->get_fail( "github/robertkrimen/gist-it-example/blob/master/Test" );
$twim->status_code_is( 404 );
$twim->body_like( qr{\QUnable to fetch "https://github.com/robertkrimen/gist-it-example/raw/master/Test": (404)\E} );

$twim->get_fail( "github/robertkrimen/gist-it-example/master/blob/README" );
diag( $body = $twim->response->content );
$twim->status_code_is( 404 );
$twim->body_like( qr{\QUnable to fetch "https://github.com/robertkrimen/gist-it-example/raw/blob/README": (404)\E} );

$twim->get_fail( "github" );
$twim->status_code_is( 404 );
$twim->body_like( qr{\QNot Found\E} );

$twim->get_fail( "xyzzy" );
$twim->status_code_is( 404 );
$twim->body_like( qr{\QNot Found\E} );

$twim->get_fail( "github/" );
$twim->status_code_is( 500 );
$twim->body_like( qr{\QUnable to parse "/github/": Not a valid repository path?\E} );
diag $twim->response->content;

for (qw[
    embed.css
    prettify/prettify.css
    prettify/prettify.js
]){
    $twim->get( "assets/$_" );
    $twim->status_code_is( 200, $_ );
}

$twim->get_fail( "xyzzy/github/robertkrimen/gist-it-example/blob/master" );
$twim->status_code_is( 500 );
$twim->body_like( qr{\QUnable to parse "github/robertkrimen/gist-it-example/blob/master": Not a valid repository path?\E} );

$twim->get( "xyzzy/github/miyagawa/CPAN-Any/blob/master/README" );
$twim->status_code_is( 200 );
$twim->body_like( qr/CPAN::Any/ );

done_testing;
