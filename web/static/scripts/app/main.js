/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       
 *                    All the interaction between the user and the UI will be handled by this class
 *                    Here we get parameters chosen by the user and then we populate the correponding modules
 * ======================================================================== */

require(["jquery","jquery.jqueryui","jquery.bootstrap","slimscroll",
            "goog!visualization,1,packages:[corechart]","dateformat",
            "modules","chart","dynatable","daterangepicker","util/helper"], 
    function($,jqueryui,bootstrap,slimscroll,jsapi,dateformat,PageModules,gPieChart,Dynatable,Daterangepicker,Helper) {

	var chart = new gPieChart(); //create Google pie chart
	chart.initializeChart(); //initilize

	var modules = new PageModules(); //Create Modules intance
    var helper = new Helper(); //create helper intance

    /* Onload method */
	$(window).load(function() {	

		
	});

    /*Document ready method */
    $(document).ready(function() {

        //Initialize slimScroll for tweet feed module
        $(function(){
            $('#scrollable').slimScroll({
                height: '250px'
            });
        });

        //Get global List of languages
        modules.populateListOfLanguages();

        //Initialize dynatable for cultures by suburb
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

        //Initialize daterange picker list box
        $('#daterange-btn').daterangepicker(helper.date_options,selectedDate);

        //Initialize date to the last 30 days
        var ini_date = moment().subtract(29, 'days');
        var end_date = moment();

        startDate = ini_date; //assign to global variable
        endDate = end_date; //assign to global variable

        //present formatted dates to the user
        $('#daterange-btn span').html(startDate.format('MMMM D, YYYY') + ' - ' + endDate.format('MMMM D, YYYY'));
        
        //Show and Hide tweet feed pages
        show("tab_1-1");
        hide("tab_2-2");
        hide("tab_3-3");

        //Populate Sentiment by City totals
        modules.populateSentimentByCityBarChart("*");
        //Populate Top trends totals by city
        modules.populateTopTrendsByCityBarChart(5);

    });


    /*When the user clicks the GO button do the following*/
	$("#go-button").click( function(e){

        //Activate flag
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
			helper.infoMessage("Please insert some topic, or * if you want to query any results");
		}
   	});

    /* Reset values, visibility, clear variables, etc */
    function clearModules(){

        helper.restartModules();

    };

    /* Collapse buttons controlling */
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

   	/*Toggle between buttons in tweet feed */
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

    //Toggle collapsable buttons on module*/
	$('#toggle-map').click(function(){
	    $(this).find('i').toggleClass('fa-plus fa-minus')
	});

    //Toggle collapsable buttons on module*/
    $('#toggle-top5-twitterers').click(function(){
        $(this).find('i').toggleClass('fa-plus fa-minus')
    });

    //Toggle collapsable buttons on module*/
    $('#toggle-top5-trends').click(function(){
        $(this).find('i').toggleClass('fa-plus fa-minus')
    });

    //Toggle collapsable buttons on module*/
    $('#toggle-top5-cultures').click(function(){
        $(this).find('i').toggleClass('fa-plus fa-minus')
    });

    //Toggle collapsable buttons on module*/
    $('#toggle-sentimentbycity').click(function(){
        $(this).find('i').toggleClass('fa-plus fa-minus')
    });

    /*Trigger click event*/
    function triggerButonClick(id){
        $("#"+id).trigger("click");
    };

    /*Event handling for tweet feed module */
    $("#btn-pos").click(function() {
    	show("tab_1-1");
        hide("tab_2-2");
        hide("tab_3-3");
    });

    /*Event handling for tweet feed module */
    $("#btn-neu").click(function() {        
		hide("tab_1-1");
		show("tab_2-2");
		hide("tab_3-3");
    });

    /*Event handling for tweet feed module */
    $("#btn-neg").click(function() {        
        hide("tab_1-1");
        hide("tab_2-2");
        show("tab_3-3");
    });

    /* Date selection callback which triggers suburb list box onchange event*/
    function selectedDate(start,end){
        startDate = start;
        endDate = end;
        console.log(startDate + ' - ' + endDate);
        $('#daterange-btn span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        $("#select-suburbs").trigger("change");
    };

    /* Generic show event*/
    function show(id){
        var selector = '#'+id;
        $(selector).fadeIn(2000);
    };

    /* Generic show event*/
    function hide(id){
        var selector = '#'+id;
        $(selector).fadeOut(100);
    };

    /* Support for pagination in tweet feed module */
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


    /* Populate suburbs list and other modules when selecting a city on the list box */
    $( "#select-cities" ).change(function() {
        
        resetDynatable(); //Clear table
        
        var term = $("#term").val(); //get the term

        //Populate list of suburbs based on the selected city
        modules.populateListOfSuburbs($(this).val()); 
        
        //Populate PieChart
        modules.populatePieChartCulturesByCity(term,$(this).val());
        //Populate Line Chart
        //Disclaimer: This methos usually tkes more that 1min as it performs a count through each suburb
        modules.populateSentimentTotalsByCity(term,$(this).val());

        show('section-piechart-cultures');
        show('section-linechart-sentiment');

    });

    /* Populate the rest of the modules which depends on the suburb selection */
    $( "#select-suburbs" ).change(function() {
        
        show("table-div");

        var term = $("#term").val();
        var state = $("#select-cities").val();
        var suburb = $(this).val();
        var date = null;

        //Populate table module
        modules.populateTable(term,state,suburb,date);
        show('section-linechart-cultures');

    });

    //Populate all modules based on the results defined on the global flag which shouldn't be empty
    $('#results-found').change(function() { 

        if ($(this).val() != 0){

            var term = $("#term").val();
            var suburb = $("#select-suburbs").val();
            var date = null;


            modules.populatePopulationVsTweetsBarChart(term);
            modules.drawTweetsBySuburb($("#term").val(),suburb);
            modules.populateTopTwitterers(term,suburb,5);
            modules.populateTopTrends(term,suburb,5);
            modules.populateChartModule(chart,term,suburb);
            modules.populateTweetModuleByTerm(term,suburb,start_page,size_page);
            
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

    //Reset table module
    function resetDynatable(){
        var dynatable = $('#table-cultures').data('dynatable');
        dynatable.settings.dataset.originalRecords = null;
        dynatable.process();
    };

    //Refresh map
    function refreshMap(){
        var center = map.getCenter();
        google.maps.event.trigger(map, "resize");
        map.setCenter(center); 
    };

    //Reset modules with initial values for new searches    
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