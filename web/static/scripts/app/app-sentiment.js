/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       
 *                    All the interaction between the user and the UI will be handled by this class
 *                    Here we get parameters chosen by the user and then we make calls to the 'modules.js' class.
 * ======================================================================== */

require(["jquery","jquery.jqueryui","jquery.bootstrap","slimscroll","goog!visualization,1,packages:[corechart]","dateformat","modules","chart","dynatable","daterangepicker","util/helper"], function($,jqueryui,bootstrap,slimscroll,jsapi,dateformat,PageModules,gPieChart,Dynatable,Daterangepicker,Helper) {

	var chart = new gPieChart();
	chart.initializeChart();

	var modules = new PageModules();
    var helper = new Helper(); 

	$(window).load(function() {	

		
	});

    function clearModules(){

        helper.restartModules();

    };

    /*Document ready initializations */
	$(document).ready(function() {

		$(function(){
		    $('#scrollable').slimScroll({
		        height: '250px'
		    });
		});

        modules.populateListOfLanguages();

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

        $('#daterange-btn').daterangepicker(helper.date_options,selectedDate);


        var ini_date = moment().subtract(29, 'days');
        var end_date = moment();

        startDate = ini_date;
        endDate = end_date;

        $('#daterange-btn span').html(startDate.format('MMMM D, YYYY') + ' - ' + endDate.format('MMMM D, YYYY'));
        

		show("tab_1-1");
        hide("tab_2-2");
        hide("tab_3-3");

        modules.populateTweetsCitiesBarChart("*");
        modules.populateTopTrendsByCity(5);

	});

    /*When the user click the GO button do the following*/
	$("#go-button").click( function(e){

        $('#results-found').val(0).trigger('change');

		var term = $("#term").val();
        //Show hidden modules
        clearModules();
        resetMapAndTable();
        refreshMap();

        //If topic is not empty start to populate data*/
		if (term!="" && term!=undefined){

            modules.populateListOfCities();
            
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

    function selectedDate(start,end){
        startDate = start;
        endDate = end;
        console.log(startDate + ' - ' + endDate);
        $('#daterange-btn span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        $("#select-suburbs").trigger("change");
    };

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
        var suburb = $('#select-suburbs').val();

    	if (pos =='top' && start_page>min){
    		start_page = start_page - size_page;
            var end_page = start_page + size_page;
            $('#label-showing').empty();
            $('#label-showing').append('Showing from ' + start_page + ' to ' + end_page + ' of  ' + total_tweets + ' tweets');
    		modules.populateTweetModuleByTerm(term,suburb,start_page,size_page);

    	}else if (pos =='bottom' && start_page <= max - size_page){
    		start_page = start_page + size_page;
            var end_page = start_page + size_page;
            $('#label-showing').empty();
            $('#label-showing').append('Showing from ' + start_page + ' to ' + end_page + ' of  ' + total_tweets + ' tweets');
    		modules.populateTweetModuleByTerm(term,suburb,start_page,size_page);
    	}

	});


    $( "#select-cities" ).change(function() {
        resetDynatable();
        var term = $("#term").val();
        modules.populateListOfSuburbs($(this).val());
        modules.populatePieChartCulturesByCity(term,$(this).val());

        modules.populateSentimentTotalsByCity(term,$(this).val());

    });

    $( "#select-suburbs" ).change(function() {
        show("table-div");

        var term = $("#term").val();
        var state = $("#select-cities").val();
        var suburb = $(this).val();
        var date = null;

        modules.populateTable(term,state,suburb,date);

    });

    $('#results-found').change(function() { 

        if ($(this).val() != 0){

            var term = $("#term").val();
            var suburb = $("#select-suburbs").val();
            var date = null;


            modules.drawTweetsBySuburb($("#term").val(),suburb);
            modules.populateTopTwitterers(term,suburb,5);
            modules.populateTopTrends(term,suburb,5);
            modules.populateChartModule(chart,term,suburb);
            modules.populateTweetModuleByTerm(term,suburb,start_page,size_page);
            // modules.populatePositivePeople(term,suburb); //Unused
            // modules.populateNegativePeople(term,suburb); //Unused

            $('#disclaimer-sentiment').delay("1500").fadeIn();
            $("#section-chart").delay("1500").fadeIn();
            $("#section-feed").delay("1500").fadeIn();
            $("#section-toptwitterers").delay("1500").fadeIn();
            $("#section-toptrends").delay("1500").fadeIn();
            $("#section-topcountries").delay("1500").fadeIn();
            $("#section-overallsentiment").delay("1500").fadeIn();
            $("#div-totals").delay("1500").fadeIn();     
            $('#section-bar-chart').css('visibility','visible').hide().fadeIn("3000");   

        }else{
            if ($('#section-toptwitterers').css('display') == 'block'){
                clearModules();
                resetMapAndTable();
                refreshMap();
            }
        }

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

    function resetMapAndTable(){
        //Clear Map
        deleteMarkers();
        map.data.forEach(function(feature) {
            //filter...
            map.data.remove(feature);
        });
        map.setCenter(new google.maps.LatLng(-26.209487, 134.060946)); 
        map.setZoom(4);

        ////Clear Map
        var dynatable = $('#table-cultures').data('dynatable');
        dynatable.settings.dataset.originalRecords = null;
        dynatable.paginationPerPage.set(8);
        dynatable.process();

    };


});