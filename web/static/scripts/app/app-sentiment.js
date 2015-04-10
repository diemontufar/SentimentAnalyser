/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       Here you can define the main method callings using jquery and JS 
 * ======================================================================== */

require(["jquery","jquery.jqueryui","jquery.bootstrap","slimscroll","goog!visualization,1,packages:[corechart]","dateformat","modules","map","chart"], function($,jqueryui,bootstrap,slimscroll,jsapi,dateformat,PageModules,Map,Chart) {

	//var map = new Map();
	//map.initializeMap();
	//console.log(map.getMap());
	var chart = new Chart();
	chart.initializeChart();
	//console.log(chart.getChart());
	var modules = new PageModules();

	$(window).load(function() {

		showTweetTab("tab_1-1");
        hideTweetTab("tab_2-2");
        hideTweetTab("tab_3-3");
		
		
	});

	$(document).ready(function() {

		$(function(){
		    $('#scrollable').slimScroll({
		        height: '250px'
		    });
		});

		modules.populateTweetModule();

	});

	$("#go-button").click( function(){

		var term = $("#term").val();
		// map.setCenter(new google.maps.LatLng(36.784844,115.446828));

		if (term!="" && term!=undefined){
			modules.populateTweetModuleByTerm(term);
			modules.populateTableModule(chart,term);
			//modules.populateChartModuleByTerm(chart);
		}else{
			console.log("Please insert some term!");
		}

   	});

   	$("[data-widget='collapse']").click(function() {
        //Find the box parent        
        var box = $(this).parents(".box").first();
        //Find the body and the footer
        var bf = box.find(".box-body, .box-footer");
        if (!box.hasClass("collapsed-box")) {
            box.addClass("collapsed-box");
            bf.slideUp();
        } else {
            box.removeClass("collapsed-box");
            bf.slideDown();
        }
    });

    $('.btn-group[data-toggle="btn-toggle"]').each(function() {
	    var group = $(this);
	    $(this).find(".btn").click(function(e) {
	        group.find(".btn.active").removeClass("active");
	        $(this).addClass("active");
	        e.preventDefault();
	    });
    });

    $("#btn-pos").click(function() {
    	showTweetTab("tab_1-1");
        hideTweetTab("tab_2-2");
        hideTweetTab("tab_3-3");
    });

    $("#btn-neu").click(function() {        
		hideTweetTab("tab_1-1");
		showTweetTab("tab_2-2");
		hideTweetTab("tab_3-3");
    });

    $("#btn-neg").click(function() {        
        hideTweetTab("tab_1-1");
        hideTweetTab("tab_2-2");
        showTweetTab("tab_3-3");
    });

    function showTweetTab(id){
    	document.getElementById(id).style.display = "block";
    };

    function hideTweetTab(id){
    	document.getElementById(id).style.display = "none";
    };

   	

});