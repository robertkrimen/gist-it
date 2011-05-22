if ( 'prettyPrint' in window ) {} else {
    document.write( '<script type="text/javascript" src="{{ base }}/assets/prettify/prettify.js"></script>' );
}
document.write( '<link rel="stylesheet" href="{{ base }}/assets/embed.css"/>' );
document.write( '<link rel="stylesheet" href="{{ base }}/assets/prettify/prettify.css"/>' );
document.write( '{{ gist_html.encode( 'string_escape' ) }}' );
document.write( '<script type="text/javascript">prettyPrint();</script>' );
