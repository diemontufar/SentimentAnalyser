/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       
 *                    All the interaction between the user and the UI will be handled by this class
 *                    Here we get parameters chosen by the user and then we make calls to the 'modules.js' class.
 * ======================================================================== */

require(["jquery","jquery.jqueryui","jquery.bootstrap","slimscroll","goog!visualization,1,packages:[corechart]","dateformat","modules","chart","dynatable","util/helper"], function($,jqueryui,bootstrap,slimscroll,jsapi,dateformat,PageModules,Chart,Dynatable,Helper) {

	var chart = new Chart();
	chart.initializeChart();

	var modules = new PageModules();
    var helper = new Helper(); 

	$(window).load(function() {	

		
	});

    /*Document ready initializations */
	$(document).ready(function() {

		$(function(){
		    $('#scrollable').slimScroll({
		        height: '250px'
		    });
		});

        $('#table-cultures').dynatable({
            features: {
                paginate: true,
                sort: true,
                pushState: true,
                search: true,
                recordCount: true,
                perPageSelect: false
              }
        });

		show("tab_1-1");
        hide("tab_2-2");
        hide("tab_3-3");

	});

    /*When the user click the GO button do the following*/
	$("#go-button").click( function(e){

		var term = $("#term").val();
        //Show hidden modules
        show("section-cultures");
        show("section-map");
        show("section-chart");
        show("section-feed");
        refreshMap();

        //If topic is not empty start to populate data*/
		if (term!="" && term!=undefined){

            modules.populateListOfCities();
			modules.populateTweetModuleByTerm(term,start_page,size_page);
			modules.populateChartModule(chart,term);
		}else{
			helper.infoMessage("Please insert some topic!");
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

    $('#toggle-cultures').click(function(){
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
        var selector = '#'+id;
        $(selector).fadeIn(2000);
    };

    function hide(id){
        var selector = '#'+id;
        $(selector).fadeOut(100);
    };

    //Pagination
    $("#scrollable").slimScroll().bind('slimscroll', function(e, pos){

    	var term = $("#term").val();
        var min = 1;
        var max = total_tweets;

    	if (pos =='top' && start_page>min){
    		start_page = start_page - size_page;
            var end_page = start_page + size_page;
            $('#label-showing').empty();
            $('#label-showing').append('Showing from ' + start_page + ' to ' + end_page + ' of  ' + total_tweets + ' tweets');
    		modules.populateTweetModuleByTerm(term,start_page,size_page);

    	}else if (pos =='bottom' && start_page <= max - size_page){
    		start_page = start_page + size_page;
            var end_page = start_page + size_page;
            $('#label-showing').empty();
            $('#label-showing').append('Showing from ' + start_page + ' to ' + end_page + ' of  ' + total_tweets + ' tweets');
    		modules.populateTweetModuleByTerm(term,start_page,size_page);
    	}

	});


    $( "#select-cities" ).change(function() {
        
        resetDynatable();
        modules.populateListOfSuburbs($(this).val());

    });

    $( "#select-suburbs" ).change(function() {
        modules.populateTableOfCultures($(this).val());
    });

    function resetDynatable(){
        var dynatable = $('#table-cultures').data('dynatable');
        dynatable.settings.dataset.originalRecords = null;
        dynatable.process();
    };

    function refreshMap(){
        var center = map.getCenter();
        google.maps.event.trigger(map, "resize");
        map.setCenter(center); 
    };


});