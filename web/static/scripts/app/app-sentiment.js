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
		
		
	});

	$(document).ready(function() {

		$(function(){
		    $('#chat-box').slimScroll({
		        height: '250px'
		    });
		});

		modules.populateTableModule(chart);
		modules.populateTweetModule();

	});

	$("#go-button").click( function(){

		var term = $("#term").val();
		// map.setCenter(new google.maps.LatLng(36.784844,115.446828));

		if (term!="" && term!=undefined){
			modules.populateTweetModuleByTerm(term);
		}else{
			console.log("Please insert some term!");
		}

   	});

   	

});