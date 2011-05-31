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
$test->body_like( qr/Try it/ );

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
$test->body_like( qr{\Q<span><a href="https://github.com/robertkrimen/gist-it-example/blob/master/example.js">This Gist</a> by <a href="$base">gist-it</a></span>\E} );
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
    960/960.css
    960/reset.css
    960/text.css
    css3buttons/css3buttons-background.png
    css3buttons/css3buttons-icon.png
    css3buttons/css3buttons.css
    embed.css
    index.js
    jquery-ui/base/jquery-ui.css
    jquery-ui/base/ui-bg_flat_0_aaaaaa_40x100.png
    jquery-ui/base/ui-bg_flat_75_ffffff_40x100.png
    jquery-ui/base/ui-bg_glass_55_fbf9ee_1x400.png
    jquery-ui/base/ui-bg_glass_65_ffffff_1x400.png
    jquery-ui/base/ui-bg_glass_75_dadada_1x400.png
    jquery-ui/base/ui-bg_glass_75_e6e6e6_1x400.png
    jquery-ui/base/ui-bg_glass_95_fef1ec_1x400.png
    jquery-ui/base/ui-bg_highlight-soft_75_cccccc_1x100.png
    jquery-ui/base/ui-icons_222222_256x240.png
    jquery-ui/base/ui-icons_2e83ff_256x240.png
    jquery-ui/base/ui-icons_454545_256x240.png
    jquery-ui/base/ui-icons_888888_256x240.png
    jquery-ui/base/ui-icons_cd0a0a_256x240.png
    jquery-ui/jquery-ui.js
    jquery.js
    spinner.gif
    prettify/prettify.css
    prettify/prettify.js
]){
    $test->get( "$base/assets/$_" );
    $test->status_code_is( 200, $_ );
}

done_testing;
