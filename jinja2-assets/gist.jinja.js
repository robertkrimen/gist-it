{% if gist.highlight == 'prettify' %}
if ( 'prettyPrint' in window ) {} else {
    document.write( '<script type="text/javascript" src="{{ base }}/assets/prettify/prettify.js"></script>' );
}
{% endif %}
{% if gist.style != '0' %}
document.write( '<link rel="stylesheet" href="{{ base }}/assets/embed.css"/>' );
{% endif %}
{% if gist.highlight == 'prettify' %}
document.write( '<link rel="stylesheet" href="{{ base }}/assets/prettify/prettify.css"/>' );
{% endif %}
document.write( '{{ gist_html.encode( 'string_escape' ) }}' );
{% if gist.highlight == 'prettify' %}
document.write( '<script type="text/javascript">prettyPrint();</script>' );
{% endif %}
