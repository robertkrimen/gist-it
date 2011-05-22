ZeroClipboard.setMoviePath( '/assets/zeroclipboard/ZeroClipboard.swf' );
var __gi_ctc = new ZeroClipboard.Client();
var __gi_ctc_text;
var __gi_timeout;

function __gi_setSource( url ) {
    if ( ! __gi_base ) {
        throw new Error( "__gi_base is undefined!" )
    }
    var text = '<script src="' + __gi_base + '/' + url + '"></script>';
    $( '#try-it-source' ).text( text );
    __gi_ctc_text = text;
}

function __gi_tryIt( result, cleanUrl ){
    clearTimeout( __gi_timeout );
    $( '#try-it-result div.gister-gist' ).remove();
    $( '#try-it-result' ).append( result );
    __gi_setSource( cleanUrl );
    $( '#try-it-load' ).text( 'Load' );
    $( '#try-it-loading' ).hide();
    prettyPrint();
}

$( function(){

    function resetTryIt(){
        var url = 'http://github.com/robertkrimen/gist-it-example/blob/master/example.js';
        $( '#try-it-field' ).val( '' );
        loadTryIt( url );
    }

    function loadTryIt( url ){
        clearTimeout( __gi_timeout );
        __gi_timeout = setTimeout( function(){
            __gi_ctc_text = '';
            $( '#try-it-load' ).text( 'Load' );
            $( '#try-it-loading' ).hide();
            $( '#try-it-source' ).html( 'Load failure &mdash; Timed out' );
        }, 12000 );
        var script = document.createElement( 'script' );
        script.type = 'text/javascript';
        script.src = "/" + url + '?callback=__gi_tryIt';
        $( '#try-it-load' ).text( 'Loading' );
        $( '#try-it-loading' ).show();
        $( 'body' ).append( script );
    }

    var egColor = $( '#try-it-eg' ).css( 'color' );
    $( '#try-it-load' ).click( function(){
        arguments[ 0 ].preventDefault();
        var value = $( '#try-it-field' ).val();
        if( value !== '' ) {
            loadTryIt( value );
        }
        else {
            $( '#try-it-eg' ).children().andSelf().animate({ color: '#f33' }, 500 ).animate({ color: egColor }, 1000 );
            $( '#try-it-field' ).effect( 'highlight', { color: '#f33' });
        }
    } );

    $( '#try-it-reset' ).click( function(){
        arguments[ 0 ].preventDefault();
        resetTryIt();
    } );

    var ctc = __gi_ctc;
    ctc.setText( '' );
    ctc.glue( 'try-it-ctc', 'try-it-ctc-zeroclipboard' );
    ctc.addEventListener( 'onMouseDown', function(){
        ctc.setText( __gi_ctc_text );
        $( ctc.div ).tipsy( 'hide' ).attr( 'title', 'Copied' ).tipsy( 'show' ).attr( 'original-title', '' );
    } );
    $( ctc.div ).tipsy({ gravity: 's', fallback: 'Copy' });

    __gi_setSource( 'robertkrimen/gist-it-example/raw/master/example.js' );
    
    prettyPrint();
} );

