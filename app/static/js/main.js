var a_r1_land = 0;
var a_r2_land = 0;
var a_r1_sample = 0;
var a_r2_sample = 0;
var a_r1_depot = 0;
var a_r2_depot = 0;
var a_r1_park = 0;
var a_r2_park = 0;
var r1_lander_counter = 0;
var r1_depot_counter = 0;
var t_r1_score_counter = 0;
var r2_lander_counter = 0;
var r2_depot_counter = 0;
var t_r2_score_counter = 0;
var e_r1_park_previous = 0;
var e_r1_score_counter = 0;
var e_r2_park_previous = 0;
var e_r2_score_counter = 0;
var r1_total_score = 0;
var r2_total_score = 0;
var matchscore = 0;

jQuery(document).ready(function() {
    $("#r1land_switch").change( function() {
       if ( $(this).is(":checked") ) {
           a_r1_land = 30;
       } else { a_r1_land = 0; }
    });
    $("#r2land_switch").change( function() {
       if ( $(this).is(":checked") ) {
           a_r2_land = 30;
       } else { a_r2_land = 0; }
    });
    $("#r1sample_switch").change( function() {
       if ( $(this).is(":checked") ) {
           a_r1_sample = 25;
       } else { a_r1_sample = 0; }
    });
    $("#r2sample_switch").change( function() {
       if ( $(this).is(":checked") ) {
           a_r2_sample = 25;
       } else { a_r2_sample = 0; }
    });
    $("#r1depot_switch").change( function() {
       if ( $(this).is(":checked") ) {
           a_r1_depot = 15;
       } else { a_r1_depot = 0; }
    });
    $("#r2depot_switch").change( function() {
       if ( $(this).is(":checked") ) {
           a_r2_depot = 15;
       } else { a_r2_depot = 0; }
    });
    $("#r1park_switch").change( function() {
       if ( $(this).is(":checked") ) {
           a_r1_park = 10;
       } else { a_r1_park = 0; }
    });
    $("#r2park_switch").change( function() {
       if ( $(this).is(":checked") ) {
           a_r2_park = 10;
       } else { a_r2_park = 0; }
    });
    $("#r1_lander_incr").click(function(){
        r1_lander_counter+=1;
        t_r1_score_counter+=5;
        $("#t_r1_lander_minerals").val(r1_lander_counter);
        $("#t_r1_teleop_score").val(t_r1_score_counter);
        $("#t_r1_teleop_score").trigger("change");
    });
    $("#r1_lander_decr").click(function(){
        r1_lander_counter-=1;
        t_r1_score_counter-=5;
        $("#t_r1_lander_minerals").val(r1_lander_counter);
        $("#t_r1_teleop_score").val(t_r1_score_counter);
        $("#t_r1_teleop_score").trigger("change");
    });
    $("#r1_depot_incr").click(function(){
        r1_depot_counter+=1;
        t_r1_score_counter+=2;
        $("#t_r1_depot_minerals").val(r1_depot_counter);
        $("#t_r1_teleop_score").val(t_r1_score_counter);
        $("#t_r1_teleop_score").trigger("change");
    });
    $("#r1_depot_decr").click(function(){
        r1_depot_counter-=1;
        t_r1_score_counter-=2;
        $("#t_r1_depot_minerals").val(r1_depot_counter);
        $("#t_r1_teleop_score").val(t_r1_score_counter);
        $("#t_r1_teleop_score").trigger("change");
    });
    $("#r2_lander_incr").click(function(){
        r2_lander_counter+=1;
        t_r2_score_counter+=5;
        $("#t_r2_lander_minerals").val(r2_lander_counter);
        $("#t_r2_teleop_score").val(t_r2_score_counter);
        $("#t_r2_teleop_score").trigger("change");
    });
    $("#r2_lander_decr").click(function(){
        r2_lander_counter-=1;
        t_r2_score_counter-=5;
        $("#t_r2_lander_minerals").val(r2_lander_counter);
        $("#t_r2_teleop_score").val(t_r2_score_counter);
        $("#t_r2_teleop_score").trigger("change");
    });
    $("#r2_depot_incr").click(function(){
        r2_depot_counter+=1;
        t_r2_score_counter+=2;
        $("#t_r2_depot_minerals").val(r2_depot_counter);
        $("#t_r2_teleop_score").val(t_r2_score_counter);
        $("#t_r2_teleop_score").trigger("change");
    });
    $("#r2_depot_decr").click(function(){
        r2_depot_counter-=1;
        t_r2_score_counter-=2;
        $("#t_r2_depot_minerals").val(r2_depot_counter);
        $("#t_r2_teleop_score").val(t_r2_score_counter);
        $("#t_r2_teleop_score").trigger("change");
    });
    $("select[name=e_r1_park]").focus(function () {
        e_r1_park_previous = this.value;
    }).change(function() {
        e_r1_score_counter+=(this.value - e_r1_park_previous);
        $("#e_r1_endgame_score").val(e_r1_score_counter);
        $('#e_r1_endgame_score').trigger('change');
        e_r1_park_previous = this.value;
    });
    $("select[name=e_r2_park]").focus(function () {
        e_r2_park_previous = this.value;
    }).change(function() {
        e_r2_score_counter+=(this.value - e_r2_park_previous);
        $("#e_r2_endgame_score").val(e_r2_score_counter);
        $('#e_r2_endgame_score').trigger('change');
        e_r2_park_previous = this.value;
    });
    $("#r1latched_switch").change( function() {
       if ( $(this).is(":checked") ) {
           e_r1_score_counter += 50;
       } else { e_r1_score_counter -= 50; }
       $("#e_r1_endgame_score").val(e_r1_score_counter);
       $('#e_r1_endgame_score').trigger('change');
       e_r1_park_previous = this.value;
    });
    $("#r2latched_switch").change( function() {
       if ( $(this).is(":checked") ) {
           e_r2_score_counter += 50;
       } else { e_r2_score_counter -= 50; }
       $("#e_r2_endgame_score").val(e_r2_score_counter);
       $('#e_r2_endgame_score').trigger('change');
       e_r2_park_previous = this.value;
    });



    $("input").change(function(){
       $("#a_r1_auto_score").val(a_r1_land + a_r1_sample + a_r1_depot + a_r1_park);
    });
    $("input").change(function(){
       $("#a_r2_auto_score").val(a_r2_land + a_r2_sample + a_r2_depot + a_r2_park);
    });
    $("input").change(function(){
        r1_total_score = a_r1_land + a_r1_sample + a_r1_depot + a_r1_park + t_r1_score_counter + e_r1_score_counter;
        matchscore = r1_total_score + r2_total_score;
        $("#r1_total_score").val(r1_total_score);
        $("#match_score").val(matchscore);
    });
    $("input").change(function(){
        r2_total_score = a_r2_land + a_r2_sample + a_r2_depot + a_r2_park + t_r2_score_counter + e_r2_score_counter;
        matchscore = r2_total_score + r1_total_score;
        $("#r2_total_score").val(r2_total_score);
        $("#match_score").val(matchscore);
    });

    // Sorting Tables
    $("#scoutingrecords").tablesorter({
        sortList: [[0,0]]
    });
    $("#scoringrecords").tablesorter({
        sortList: [[2,1]]
    });
    $("#scoutingreport").tablesorter({
        sortList: [[4,0]]
    });
    $("#table-sparkline").tablesorter({
        sortList: [[2,1]]
    });

});
