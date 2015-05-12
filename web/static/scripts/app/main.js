/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       
 *                    All the interaction between the user and the UI will be handled by this class
 *                    Here we get parameters chosen by the user and then we populate the correponding modules
 * ======================================================================== */

require(["jquery","jquery.jqueryui","jquery.bootstrap","slimscroll",
            "goog!visualization,1,packages:[corechart]","dateformat",
            "modules","dynatable","daterangepicker","util/helper"], 
    function($,jqueryui,bootstrap,slimscroll,jsapi,dateformat,PageModules,Dynatable,Daterangepicker,Helper) {

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
                search: false,
                recordCount: true,
                perPageSelect: false
              }
        });

        //Initialize daterange picker list box
        $('#daterange-btn').daterangepicker(helper.date_options,selectedDate);

        //Initialize date to the last 30 days
        var ini_date = moment().subtract(6, 'days');
        var end_date = moment();

        startDate = ini_date; //assign to global variable
        endDate = end_date; //assign to global variable

        //present formatted dates to the user
        var dateStr = helper.getDateRange(startDate,endDate);
        $('#daterange-btn span').html(dateStr);
        
        //Show and Hide tweet feed pages
        show("tab_1-1");
        hide("tab_2-2");
        hide("tab_3-3");

        updateSentimentAndTrendsByCity();

    });


    //When the user presses the execute cluster button */
    $("#cluster-button").on('click', function(e){

        var term = $("#term").val();
        //If topic is not empty start to populate data*/
        if (term=="" || term===undefined || term===null){
            helper.errorMessage("Please insert some topic if you want to query any results");
            return;
        }

        var dateStr = helper.getDateRange(startDate,endDate);
        var msg = "<b>Are you sure do you want to execute the Lingo clustering algorithm?</b><br><br>";
        msg += "<b>Term:&nbsp;</b>" + term;
        msg += "<br><b>Period:&nbsp;</b>" + dateStr;

        var icon = '<i class="icon fa fa-warning" style="margin-right: 10px;"></i>';
        $('.modal-title').empty();
        $('.modal-body').empty();
        $('.modal-title').append(icon+'Warning');
        $('.modal-body').append(msg);

        $('#confirmationModal').modal('show');

        $('#confirmationModal').modal({ backdrop: 'static', keyboard: false })
            .one('click', '#execute', function (e) {
                console.log("I'm going to execute the Algorithm");
                triggerButonClick("toggle-cluster");
                modules.populateCluster(term);
            });
    });

    //When the user presses the execute sentiment totals button */
    $("#sentiment-totals-button").on('click', function(e){

        var term = $("#term").val();
        //If topic is not empty start to populate data*/
        if (term=="" || term===undefined || term===null){
            helper.errorMessage("Please insert some topic if you want to query any results");
            return;
        }

        var state = $('#select-cities').val();

        //If topic is not empty start to populate data*/
        if (state=="" || state===undefined || state===null){
            helper.errorMessage("City is required, please select one from the list first");
            return;
        }

        var city = $( "#select-cities option:selected" ).text();

        var dateStr = helper.getDateRange(startDate,endDate);
        var msg = "<b>Are you sure do you want to execute total Sentiment statistics by Suburb?</b><br><br>";
        msg += "<b>Term:&nbsp;</b>" + term;
        msg += "<br><b>City:&nbsp;</b>" + city;
        msg += "<br><b>Period:&nbsp;</b>" + dateStr;

        var icon = '<i class="icon fa fa-warning" style="margin-right: 10px;"></i>';
        $('.modal-title').empty();
        $('.modal-body').empty();
        $('.modal-title').append(icon+'Warning');
        $('.modal-body').append(msg);

        $('#confirmationModal').modal('show');

        $('#confirmationModal').modal({ backdrop: 'static', keyboard: false })
            .one('click', '#execute', function (e) {
                console.log("I'm going to execute sentiment totals by suburb");
                triggerButonClick("toggle-sentimentbycity");
                modules.populateSentimentTotalsByCity(term,state);
            });
    });


    /*When the user clicks the GO button do the following*/
	$("#go-button").click( function(e){

        //Activate flag
        $('#results-found').val(0).trigger('change');
        var helper = new Helper();

		var term = $("#term").val();
        var state = $('#select-cities').val();
        var suburb = $('#select-suburbs').val();

        //If topic is not empty start to populate data*/
        if (term=="" || term===undefined || term===null){
            helper.errorMessage("Please insert some topic if you want to query any results");
            return;
        }

        if (state === null && suburb===null){ //First time search
            modules.populateListOfCities();
            showFirstTime();
            updateSentimentAndTrendsByCity();   
        }

        if (state !== null && suburb===null){ //Is not the first time but suburb is missing
            helper.errorMessage('Suburb cannot be empty, please select one from the list');
        }else if(state !== null && suburb!==null){
            console.log(state);
            console.log(suburb);

            $("#select-suburbs").trigger("change");
        }else{
            helper.alertMessage('Some modules require City and Suburb parameters, please select one from the list');
        }

   	});

    function showFirstTime(){
        $("#section-cultures").fadeIn(2000);
        $("#section-map").fadeIn(2000);
        refreshMap();
    };

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

    //Toggle collapsable buttons on module*/
    $('#toggle-cluster').click(function(){
        $(this).find('i').toggleClass('fa-plus fa-minus')
    });

    //Toggle collapsable buttons on module*/
    $('#toggle-culturesbycity-bar').click(function(){
        $(this).find('i').toggleClass('fa-plus fa-minus')
    });

    //Toggle collapsable buttons on module*/
    $('#toggle-culturesbycity-pie').click(function(){
        $(this).find('i').toggleClass('fa-plus fa-minus')
    });

    $(document).keypress(function(e) {
        if(e.which == 13) {
            $("#go-button").trigger("click");
        }
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
        var dateStr = helper.getDateRange(startDate,endDate);
        $('#daterange-btn span').html(dateStr);

        var state = $('#select-cities').val();
        var suburb = $('#select-suburbs').val();

        console.log(state);
        console.log(suburb);

        if (state === null && suburb===null){ //First time search
            updateSentimentAndTrendsByCity();
            return;
        }

        if (state !== null){
            updateSentimentAndTrendsByCity();
        }else{
            helper.errorMessage('City cannot be empty, please select one from the list');
        }

        if ( suburb === null){
            helper.alertMessage('Some modules require Suburb as parameter, please select one from the list');
        }else{
            var term = $("#term").val();
            if (term === null || term === undefined || term === ""){
                term = "*";
            }
            updateCulturesTotalsSentimentAndTrends(term,state);
            $("#select-suburbs").trigger("change");
        }

    };

    /* Update modules of totals */
    function updateSentimentAndTrendsByCity(){
        //Populate Sentiment by City totals
        var term = $("#term").val();
        if (term === null || term === undefined || term === ""){
            term = "*";
        }
        modules.populateSentimentByCityBarChart(term);
        //Populate Top trends totals by city
        modules.populateTopTrendsByCityBarChart(5);
    };

    /* Update modules:
    *       populatePieChartCulturesByCity
    *       updateSentimentAndTrendsByCity
    */
    function updateCulturesTotalsSentimentAndTrends(term,stateCode){
        //Populate PieChart
        modules.populatePieChartCulturesByCity(term,stateCode);

        //Populate modules of totals (Sentiment and Top Trends)
        updateSentimentAndTrendsByCity();

        show('section-piechart-cultures');
        show('section-linechart-cultures');

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
        
        $('#results-found').val(0).trigger('change');
        resetDynatable(); //Clear table
        
        var term = $("#term").val(); //get the term

        //Populate list of suburbs based on the selected city
        modules.populateListOfSuburbs($(this).val()); 

        updateCulturesTotalsSentimentAndTrends(term,$(this).val());

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
        updateSentimentAndTrendsByCity();

    });

    //Populate all modules based on the results defined on the global flag which shouldn't be empty
    $('#results-found').change(function() { 

        if ($(this).val() != 0){

            var term = $("#term").val();
            var suburb = $("#select-suburbs").val();
            var suburbName = $( "#select-suburbs option:selected" ).text();
            var date = null;


            modules.populatePopulationVsTweetsBarChart(term);
            modules.drawTweetsBySuburb($("#term").val(),suburb);
            modules.populateTopTwitterers(term,suburb,5);
            modules.populateTopTrends(term,suburb,5);
            modules.populateChartModule(term,suburb);
            modules.populateTweetModuleByTerm(term,suburb,start_page,size_page);
            
            $('#section-piechart-cultures').delay("1500").fadeIn();
            $('#section-linechart-cultures').delay("1500").fadeIn();

            //Disclaimer messages
            $('#disclaimer-sentiment').delay("1500").fadeIn();
            showLabel('#label-trends',"Top trending lists in: " + suburbName);
            $('#disclaimer-trends').delay("1500").fadeIn();

            $("#section-chart").delay("1500").fadeIn();
            $("#section-feed").delay("1500").fadeIn();
            $("#section-toptwitterers").delay("1500").fadeIn();
            $("#section-toptrends").delay("1500").fadeIn();
            $("#section-topcountries").delay("1500").fadeIn();
            // $("#section-overallsentiment").delay("1500").fadeIn();
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

    //Show label
    function showLabel(id,text){
        $(id).empty();
        $(id).append(text);
    };

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
        // map.data.forEach(function(feature) {
        //     //filter...
        //     map.data.remove(feature);
        // });
        map.setCenter(new google.maps.LatLng(-26.209487, 134.060946)); 
        map.setZoom(4);

        ////Clear Map
        var dynatable = $('#table-cultures').data('dynatable');
        dynatable.settings.dataset.originalRecords = null;
        dynatable.paginationPerPage.set(8);
        dynatable.process();

    };


});