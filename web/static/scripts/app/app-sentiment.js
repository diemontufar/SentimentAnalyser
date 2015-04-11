/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       Here you can define the main method callings using jquery and JS 
 * ======================================================================== */

require(["jquery","jquery.jqueryui","jquery.bootstrap","slimscroll","goog!visualization,1,packages:[corechart]","dateformat","modules","chart"], function($,jqueryui,bootstrap,slimscroll,jsapi,dateformat,PageModules,Chart) {

	var chart = new Chart();
	chart.initializeChart();

	var modules = new PageModules();

	$(window).load(function() {	

		
	});

	$(document).ready(function() {

		$(function(){
		    $('#scrollable').slimScroll({
		        height: '250px'
		    });
		});

        hide("section-chart");
        hide("section-feed");

		show("tab_1-1");
        hide("tab_2-2");
        hide("tab_3-3");

	});

	$("#go-button").click( function(e){

		var term = $("#term").val();
        show("section-chart");
        show("section-feed");

		if (term!="" && term!=undefined){
			modules.populateTweetModuleByTerm(term,start_page,size_page);
			modules.populateTableModule(chart,term);
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

   	//Toggle between button in tweet feed
    $('.btn-group[data-toggle="btn-toggle"]').each(function() {
	    var group = $(this);
	    $(this).find(".btn").click(function(e) {
	        group.find(".btn.active").removeClass("active");
	        $(this).addClass("active");
	        e.preventDefault();
	    });
    });

    //Activate tooltips
    $("[data-toggle='tooltip']").tooltip();

	$('#toggle-map').click(function(){
	    $(this).find('i').toggleClass('fa-plus fa-minus')
	});


    $("#btn-pos").click(function() {
    	show("tab_1-1");
        hide("tab_2-2");
        hide("tab_3-3");
    });

    $("#btn-neu").click(function() {        
		hide("tab_1-1");
		show("tab_2-2");
		hide("tab_3-3");
    });

    $("#btn-neg").click(function() {        
        hide("tab_1-1");
        hide("tab_2-2");
        show("tab_3-3");
    });

    function show(id){
    	document.getElementById(id).style.display = "block";
    };

    function hide(id){
    	document.getElementById(id).style.display = "none";
    };

    //Pagination
    $("#scrollable").slimScroll().bind('slimscroll', function(e, pos){

    	var term = $("#term").val();
    	
    	if (pos =='top'){
    		start_page = start_page - size_page;
    		if (start_page >= 1){
	    		console.log("New pages top-> start: " + start_page + ", size: " + size_page);
	    		modules.populateTweetModuleByTerm(term,start_page,size_page);
	    	}
    	}else{
    		start_page = start_page + size_page;
    		if (start_page <= total_tweets){
	    		console.log("New pages Botton-> start: " + start_page + ", size: " + size_page);
	    		modules.populateTweetModuleByTerm(term,start_page,size_page);
    		}
    	}

	});


});