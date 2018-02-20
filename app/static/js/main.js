var a1 = 0;
var a1m = 0;
var a2 = 0;
var a2m = 0;
var a3 = 0;
var a4 = 0;
var t1 = 0;
var t1m = 0;
var t2 = 0;
var t3 = 0;
var t4 = 0;
var t5 = 0;
var t5m = 0;
var t6 = 0;

jQuery(document).ready(function() {
    $("#a_jewel").change( function() {
       if ( $(this).is(":checked") ) {
           a1 = 30;
       } else { a1 = 0; }
    });
    $("#a_glyphs").change( function() {
        a2 = parseInt($(this).val()) * 15;
    });
    $("#a_hit_jewel").change( function() {
       if ( $(this).is(":checked") ) {
           a1m = 30;
       } else { a1m = 0; }
    });
    $("#a_glyphs_delivered").change( function() {
        a2m = parseInt($(this).val()) * 15;
    });
    $("#a_glyph_correct").change( function() {
       if ( $(this).is(":checked") ) {
           a3 = 30;
       } else { a3 = 0; }
    });
    $("#a_park").change( function() {
       if ( $(this).is(":checked") ) {
           a4 = 10;
       } else { a4 = 0; }
    });
    $("#t_glyphs").change( function() {
        t1 = parseInt($(this).val()) * 2;
    });
    $("#t_glyphs_delivered").change( function() {
        t1m = parseInt($(this).val()) * 2;
    });
    $("#t_crypto_columns").change( function() {
        t2 = parseInt($(this).val()) * 20;
    });
    $("#t_crypto_rows").change( function() {
        t3 = parseInt($(this).val()) * 10;
    });
    $("#t_crypto_cipher").change( function() {
       if ( $(this).is(":checked") ) {
           t4 = 30;
       } else { t4 = 0; }
    });
    $("select[name=t_relic1]").change(function() {
        t5 = parseInt($(this).val());
        $('#score_projection').trigger('change');
        $('#t_score').trigger('change');
        $('#total_score').trigger('change');
    });
    $("select[name=t_relic2]").change(function() {
        t5m = parseInt($(this).val());
        $('#score_projection').trigger('change');
        $('#t_score').trigger('change');
        $('#total_score').trigger('change');
    });
    $("#t_park").change( function() {
       if ( $(this).is(":checked") ) {
           t6 = 20;
       } else { t6 = 0; }
    });
    $("input").change(function(){
        // console.log(a1, a2, a3, a4, t1, t2, t3, t4, t5, t6 );
        $("#score_projection").val(a1 + a2 + a3 + a4 + t1 + t2 + t3 + t4 + t5 + t5m + t6);
    });
    $("input").change(function(){
       $("#a_score").val(a1m + a2m + a3 + a4);
    });
    $("input").change(function(){
       $("#t_score").val(t1m + t2 + t3 + t4 + t5 + t5m + t6);
    });
    $("input").change(function(){
       $("#total_score").val(a1m + a2m + a3 + a4 + t1m + t2 + t3 + t4 + t5 + t5m + t6);
    });

    $("#matchreport").tablesorter({
            sortList: [[1,1]] // etc.

    });

    $('table.sticky-header').floatThead();
});
