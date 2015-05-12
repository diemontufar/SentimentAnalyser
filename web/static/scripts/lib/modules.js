/* ========================================================================
 * Author:            Diego Montufar
 * Date:              Feb/2015
 * Description:       The modules class calls web services served by the indexer module.
 *                    With the information obtained, populates the corresponding modules 
 *                    depending on user input in the form of a table, chart or list. 
 *                    This class interacts directly with the Helper class.
 * ======================================================================== */

define(["util/helper","highcharts","highcharts3d","exporting","nodatatodisplay","foamtree"], function(Helper,Highcharts,Highcharts3d,Exporting,Nodatatodisplay,Foamtree)
{
  "use strict";

  var default_img_avatar = "../static/img/undefined.png";

  var PageModule = function()
  {
    return {

        /*Web services URL definitions */
        //1. Used for populating Cities list box:
        suburbs_service_url : '/suburbsByCountry/',
        //2. Used to populate Suburbs list box, and a global object containing alla info about suburbs:                
        cultures_service_url : '/culturesByState', 
        //3. Used to populate a global object containing a list of languages:                   
        languages_service_url : '/languagesByCountry/',
        //4. USed to populate a bar chart with a count of sentiment results by City
        sentimenttotals_by_city_service_url: '/sentimentTotalsByCity/', 
        //5. Populate top N trends by city
        list_top_by_city_service_url: '/topListByCity/',
        //6. Populate top 5 trends/twitterers by suburb
        list_top_by_suburb_service_url: '/topListBySuburb/', 
        //7. Generic geo search with pagination
        geo_search_service_url : '/genericGeoSearch/', 
        //8. Sentiment analysis totals by suburb (Google Pie chart)
        sentiment_totals_service_url : '/sentimentTotals/',
        //9. Populate table of cultures of Australia
        table_cultures_service_url : '/tweetsByCountryOfBirth/',
        //10. Populate culture totals by city
        cultures_totals_by_city_service_url: '/cultureTotalsByCity/',
        //11. Populate sentiment totals line chart
        sentiment_totals_by_city_service_url: '/sentimentTotalsByCity/',

        //Clustering using carrot elasticsearch service
        clustering_url: 'http://115.146.86.249:9200/australia/tweet/_search_with_clusters',
        // clustering_url: 'http://localhost:9200/twitterall/tweet/_search_with_clusters',


        initialize : function() {

        },

        /* 
        * Name:         populateListOfCities
        * Module:       Cities list box
        * Parameters:   None
        * Description:  Obtain list of Cities by state from the suburbs database and filtering them by the states defined on the helper class   
        * Action:       Populate #select-cities
        * Output:       None
        */
        populateListOfCities : function(){

          var helper = new Helper();
          $('#select-suburbs').empty();
          $('#select-cities').empty();
          var country_code = "1"; //Australia

          $.getJSON(this.suburbs_service_url + country_code).done(function(data) {

            var city_options_html =  '<option value="all" disabled selected style="display:none;">Main Cities</option>';

              $.each(data.states, function(sta, state) {

                if (helper.isInStateList(state.state)){

                    city_options_html = city_options_html + '<option value="' + state.state + '">' + helper.getCityName(state.state) + '</option>';

                }

              });
               // Append html string to cities option list
              $('#select-cities').append(city_options_html);

          }).fail(function(){
            var helper = new Helper();
            helper.errorMessage('Error Loading list of Cities');
          });

        },

        /* 
        * Name:         populateListOfSuburbs
        * Module:       Suburbs list box
        * Parameters:   state (String) -> state code i.e. VIC, TAS, NSW
        * Description:  Obtain a list ob suburbs corresponding to a particular state
        * Action:       Populate #select-suburbs
        * Output:       None
        */
        populateListOfSuburbs : function(state){

          $('#select-suburbs').empty();
          cultures = null;

          $.getJSON(this.cultures_service_url+'/'+state).done(function(data) {

            if (data !== null && data!==undefined){

               var suburbs_options_html =  '<option value="all" disabled selected style="display:none;">Select a Suburb</option>';

               var lat = data.crs.properties.state_coordinate[0];
               var lang = data.crs.properties.state_coordinate[1];
               var zoom = data.crs.properties.state_coordinate[2];

               $.each(data.features, function(fea, feature) {

                  suburbs_options_html = suburbs_options_html + '<option value="' + feature.properties.feature_code + '">' + feature.properties.feature_name + '</option>';

               });

              cultures = data; //assign current result to the global variable
              map.data.addGeoJson(data);
              map.setCenter(new google.maps.LatLng(lat, lang));
              map.setZoom(zoom);
               // Append html string to suburb option list
              $('#select-suburbs').append(suburbs_options_html);

            }
          }).fail(function(){
            var helper = new Helper();
            var city = $('#select-cities :selected').text();
            helper.infoMessage('No suburbs found in: ' + city );
          });

        },

        /* 
        * Name:         populateListOfLanguages
        * Module:       Populate global variable of languages
        * Parameters:   None
        * Description:  Get a list of available languages defined on the languages couchdb
        * Action:        Populate global variable languagesGlobal
        * Output:       None
        */
        populateListOfLanguages: function(){

          $.getJSON(this.languages_service_url + '1', function(data) {

            languagesGlobal = data;

          });

        },

        /* 
        * Name:         populateSentimentByCityBarChart
        * Module:       Populate sentiment by city
        * Parameters:   term (String) -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        * Description:  Populate Sentiment by City bar chart
        * Action:        Populate #mySentimentResultsByCityChartContainer
        * Output:       None
        */
        populateSentimentByCityBarChart: function(term){

          if (startDate === null && startDate === undefined){
              startDate = moment().subtract(29, 'days');
          
            }

            if (endDate ===null && endDate ===undefined){
              endDate = moment();
            }

          //Then Build the URL in order to send to the python service:
          var request = this.sentimenttotals_by_city_service_url + term + '/' + startDate + '/' + endDate;

          $.getJSON(request, function(data) {

            var helper = new Helper();

            // console.log("Start: " + startDate.format('YYYY-MMMM-D') + ", End: " + endDate.format('YYYY-MMMM-D'));

            var title = "Count of Tweets by City: " + helper.getDateRange(startDate,endDate);

            var dataChart = helper.getTweetsByCityBarChartData(data,title,"No. of Tweets");

            $('#mySentimentResultsByCityChartContainer').highcharts(dataChart);

          });

          
        },

      /* 
        * Name:         populateTopTrendsByCityBarChart
        * Module:       Top trends by city
        * Parameters:   size (Int) ->  Top N, i.e. 5 for a top five listing
        * Description:  Get the top N list of trends by city
        * Action:        Populate #myTrendsByCityChartContainer
        * Output:       None
        */
        populateTopTrendsByCityBarChart: function(size){

          if (startDate === null && startDate === undefined){
              startDate = moment().subtract(29, 'days');
          
            }

            if (endDate ===null && endDate ===undefined){
              endDate = moment();
            }

          //Then Build the URL in order to send to the python service:
          var request = this.list_top_by_city_service_url + 'entities.hashtags.text/' + size + '/' + startDate + '/' + endDate;

          $.getJSON(request, function(data) {

            var helper = new Helper();

            var title = "Count of Tweets by City: " + helper.getDateRange(startDate,endDate);

            var dataChart = helper.getTopTrendsByCityBarChartData(data,"#",title,"% of Tweets");

            $('#myTrendsByCityChartContainer').highcharts(dataChart);


          });

        },


        /* 
        * Name:         populateTopTwitterers
        * Module:       Top twitterers list
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        *               suburb(String)  -> Suburb code. i.e. 206041122
        *               size (Int)      -> Top N, i.e. 5 for a top five listing
        * Description:  Populate Top 5 list of twitterers
        * Action:        populate #toptwitterers-div
        * Output:       None
        */
        populateTopTwitterers: function(term,suburb,size) { 

          var field = "user.screen_name";

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          var request = this.list_top_by_suburb_service_url + term + '/' + suburb + '/' + field + '/' + size + '/' + startDate + '/' + endDate;

          $.getJSON(request).done(function(data) {

            $('#toptwitterers-div').empty();
            var buckets = data.aggregations['2'].buckets;
            var html_user = '<ol type="1">';

            if ( buckets.length !=0 ){
              $.each(buckets, function(key, hit) {

                var user = "@" + hit.key;
                var url = "http://www.twitter.com/" + hit.key;

                html_user += '<li><h4><a href=' + url + ' target="_blank" class="name">' + user + '</a></h4></li>';

              });
            }else{
              var helper = new Helper();
              helper.infoMessage('No twitterers found for this topic');
            }
            
            html_user += '</ol>';
            $('#toptwitterers-div').append(html_user);

          }).fail(function(){
            var helper = new Helper();
            helper.errorMessage('Error Loading Top Tweetterers');
          });

        },

        /* 
        * Name:         populateTopTrends
        * Module:       Top trends list
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        *               suburb(String)  -> Suburb code. i.e. 206041122
        *               size (Int)      -> Top N, i.e. 5 for a top five listing
        * Description:  Populate Top 5 list of twitterers
        * Action:        populate #toptrends-div
        * Output:       None
        */
        populateTopTrends: function(term,suburb,size) { 

          var field = "entities.hashtags.text";

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          var request = this.list_top_by_suburb_service_url + term + '/' + suburb + '/' + field + '/' + size + '/' + startDate + '/' + endDate;

          $.getJSON(request).done(function(data) {

            $('#toptrends-div').empty();
            var buckets = data.aggregations['2'].buckets;
            var html_user = '<ol type="1">';

            if ( buckets.length !=0 ){
              $.each(buckets, function(key, hit) {

                var hashtag = "#" + hit.key;
                var url = " https://twitter.com/hashtag/" + hit.key;

                html_user += '<li><h4><a href=' + url + '?src=tren target="_blank" class="name">' + hashtag + '</a></h4></li>';

              });
            }else{
              var helper = new Helper();
              helper.infoMessage('No trends found for this topic');
            }
            
            html_user += '</ol>';
            $('#toptrends-div').append(html_user);

          }).fail(function(){
            var helper = new Helper();
            helper.errorMessage('Error Loading Top Trends');
          });

        },

        /* 
        * Name:         populateTweetModuleByTerm
        * Module:       Tweets
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        *               suburb(String)  -> Suburb code. i.e. 206041122
        *               start (Int)     -> Support for pagination, starting by 0 up to size
        *               size (Int)      -> Top N, i.e. 5 for a top five listing
        * Description:  Populate tweet feed module
        * Action:        
        * Output:       
        */
        populateTweetModuleByTerm: function(term,suburb,start,size) { 

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          //Then Build the URL in order to send to the python service:
          var request = this.geo_search_service_url + term + '/' + suburb + '/' +  start + '/' + size + '/' + startDate + '/' + endDate;

          // Send JSON request
          // The returned JSON object will have a property called "hits" where we find
          // a list of the tweets matching our request query
          $.getJSON(request, function(data) {

              if (data) {
                  $('#tab_1-1').empty();
                  $('#tab_2-2').empty();
                  $('#tab_3-3').empty();

                  var count_records = 0;

                $.each(data.hits.hits, function(key, hit) {

                    var tweet = hit._source;

                    // Before we continue we check that we got data
                    if (tweet.text !== undefined && tweet != null) {
                        // Calculate how many hours ago was the tweet posted
                        var date_tweet = new Date(tweet.created_at);
                        var date_locale = date_tweet.format(' H:i:s - d M Y');


                        // Build the html string for the current tweet
                        var helper = new Helper();
                        var tweet_text = helper.parseLinks(tweet.text);
                        tweet_text = helper.parseHashTags(tweet_text);
                        tweet_text = helper.parseUser(tweet_text);

                        var sentiment_analysis = tweet.sentiment_analysis;
                        var icon;
                        var _class;
                        var position;

                        if (sentiment_analysis!=null && sentiment_analysis!=undefined){
                          if (sentiment_analysis.sentiment=='positive'){
                            icon = helper.sentiment_icon.positive;
                            _class = "positive";
                          }else if(sentiment_analysis.sentiment=='negative'){
                            icon = helper.sentiment_icon.negative;
                            _class = "negative";
                          }else if(sentiment_analysis.sentiment=='neutral'){
                            icon = helper.sentiment_icon.neutral;
                            _class = "neutral";
                          }
                        }else{
                          icon = "";
                        }

                        var tweet_html = '<div class="item">';
                        tweet_html += '<img src="' + tweet.user.profile_image_url + '"' + ' onerror="this.src=\'' + default_img_avatar + "\'" + '" alt="user image" class="' + _class + '">';
                        tweet_html += '<p class="message">';
                        tweet_html += '<a href="http://www.twitter.com/' + tweet.user.screen_name + '" class="name">';
                        tweet_html += '<small class="text-muted pull-right"><i class="fa fa-clock-o"><\/i>' + date_locale + '<\/small>';
                        tweet_html += tweet.user.name + '<\/a>';
                        tweet_html += '<small class="text-muted">' + '@' + tweet.user.screen_name + '<\/small><br>';
                        tweet_html += tweet_text;
                        tweet_html += '<\/p><div class="attachment">';
                        tweet_html += '<small class="text-muted">Retweets: ' + tweet.retweet_count + ' | Favorites: ' + tweet.favorite_count + ' | Sentiment: <i class="fa ' + icon + '"><\/i><\/small>';
                        tweet_html += '<\/div><\/div>';

                        // Append html string to tweet_container div
                       if (sentiment_analysis!=null && sentiment_analysis!=undefined){
                          if (sentiment_analysis.sentiment=='positive'){
                            $('#tab_1-1').append(tweet_html);
                            count_records++;
                          }else if(sentiment_analysis.sentiment=='negative'){
                            $('#tab_3-3').append(tweet_html);
                            count_records++;
                          }else if(sentiment_analysis.sentiment=='neutral'){
                            $('#tab_2-2').append(tweet_html);
                            count_records++;
                          }
                        }
                    
                    }
                    
                });
              }

              console.log("Number of tweets on Feed module: " + count_records);

          }); //End getJSON

        },

       /* 
        * Name:         populateChartModule
        * Module:       Sentiment results by suburb
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        *               suburb(String)  -> Suburb code. i.e. 206041122  
        * Description:  Populate sentiment results: % positives, % neatives, %neutrals
        * Action:        
        * Output:       
        */
        populateChartModule : function(term,suburb){

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          //Then Build the URL in order to send to the python service:
          var request = this.sentiment_totals_service_url.concat(term + '/' + suburb + '/' + startDate + '/' + endDate);

          $.getJSON(request,function(data) {

                var helper = new Helper();

                if (data !== undefined && data !== null){

                  $.each(data, function(res, result) {

                    var chart_results = google.visualization.arrayToDataTable([
                      ['Results', 'Totals per Sentiment'],
                      ['Positive',  parseInt(result.total_positive)],
                      ['Negative',  parseInt(result.total_negative)],
                      ['Neutral',   parseInt(result.total_neutral)]
                    ]);

                    total_tweets = parseInt(result.total_positive) + parseInt(result.total_negative) + parseInt(result.total_neutral); //Update global variable
                     
                    var suburb = $( "#select-suburbs option:selected" ).text();
                    var title = "Setiment Analysis: " + suburb;

                    console.log(data);

                    var dataChart = helper.getChartModuleData(data,title);

                    $('#piechart_3d').highcharts(dataChart);

                    $('#label-showing').empty();
                    $('#label-showing').append('Showing from 1 to ' + size_page + ' of  ' + total_tweets + ' tweets');
                   
                 });
              }

        	}); //End getJSON

        },

        /* 
        * Name:         populateTable
        * Module:       AU Cultures table
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        *               state (String)  -> state code i.e. VIC,TAS,NSW, etc
        *               suburb(String)  -> Suburb code. i.e. 206041122  
        * Description:  Populate table of cultures using dynatable plugin
        * Action:       Populate #table-cultures
        * Output:       None
        */
        populateTable: function(term,state,suburb){

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          //Then Build the URL in order to send to the python service:
          var request = this.table_cultures_service_url.concat(term + '/' + state + '/' + suburb + '/' + startDate + '/' + endDate); //date missing
          tableRecordsGlobal = null;
          var totalSumRecords = 0;

          $.getJSON(request, function(data) {

            var countryRecords = data["buckets"];

            if (countryRecords){

              var helper = new Helper();
              var tableRecords = helper.getCulturesRecords(countryRecords);
              tableRecordsGlobal = tableRecords;
              tableRecordsGlobal = tableRecordsGlobal.sort(function(a,b) { return parseFloat(b.tweets) - parseFloat(a.tweets) } );

              //Populate Top 5 
               $('#topcountries-div').empty();
               var html_cultures = '<ol type="1">';

               $.each(tableRecordsGlobal,function(key,record){
                  totalSumRecords += record.tweets;
               });

               var i = 0;
               $.each(tableRecordsGlobal,function(key,record){

                  if (i<5 && record.tweets != 0){
                    html_cultures += '<li><h5>' + record.countryOfBirth + '</h5></li>';
                    i++;
                  }

               });

               html_cultures += '</ol>';
               $('#topcountries-div').append(html_cultures);

              
               if (totalSumRecords !=0){
                 var dynatable = $('#table-cultures').data('dynatable');
                 dynatable.settings.dataset.originalRecords = tableRecords;
                 dynatable.paginationPerPage.set(8);
                 dynatable.process();
               }else{
                var suburb = $('#select-suburbs :selected').text();
                var term = $("#term").val();
                helper.infoMessage('No results found for: "' + term + '" in suburb: ' + suburb);
               }

               $('#results-found').val(totalSumRecords).trigger('change');
               console.log("Total tweets listed on Table: " + totalSumRecords);

            }else{
              var suburb = $('#select-suburbs :selected').text();
              helper.infoMessage('Cultures table cannot be populated for: ' + suburb );
            }

          });

        },

        /* 
        * Name:         drawTweetsBySuburb
        * Module:       Maps
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        *               suburb(String)  -> Suburb code. i.e. 206041122
        * Description:  Populate GMaps module
        * Action:       Populate maps with markers and geojson information
        * Output:       None
        */
        drawTweetsBySuburb : function(term,suburb){

          var startP = 0;
          var sizeP = 10000;

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          //Then Build the URL in order to send to the python service:
          var request = this.geo_search_service_url + term + '/' + suburb + '/' + startP + '/' + sizeP + '/' + startDate + '/' + endDate;

          $.getJSON(request, function(data) {

            var reposition_lang = undefined;
            var reposition_lat = undefined;
            var got_center = true;

            var total_retrieved_tweets = 0;

            var mapLanguages = [];

              if (data) {

                  var helper = new Helper();
                  deleteMarkers();

                  $.each(data.hits.hits, function(key, hit) {

                    var tweet = hit._source;

                    // Before we continue we check that we got data
                    if (tweet !== undefined && tweet !== null) {
                        // Calculate how many hours ago was the tweet posted
                        var date_tweet = new Date(tweet.created_at);
                        var date_locale = date_tweet.format(' H:i:s - d M Y');

                        var lan = tweet.user.lang.toLowerCase();

                        if (lan === undefined || lan === null){
                          lan = 'und';
                        }

                        mapLanguages[lan] = (mapLanguages[lan]||0)+1;
                        total_retrieved_tweets++;

                        var marker = helper.getGeoMarkerPoint(tweet);
                        addMarker(marker); //Add markers to the map and the markers array
                        
                        if (got_center){
                            reposition_lang = marker.position.F;
                            reposition_lat = marker.position.A;
                            got_center = false;
                        }
                        
                    }else{
                      console.log("Undefined");
                    }

                  }); //inner inner each

              console.log(mapLanguages);
              console.log("Total drawn tweets: " + total_retrieved_tweets);
              var helper = new Helper();
              setAllMap(map); //Add all markers to the map
              // console.log("Lat: " + reposition_lat + " , Lat: " + reposition_lang);
              map.setCenter(new google.maps.LatLng(reposition_lat, reposition_lang)); 
              map.setZoom(12);
              } //if data
          }); //End getJSON
        },


      /* 
        * Name:         populatePieChartCulturesByCity
        * Module:       Cultures by City
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        *               state (String)  -> state code i.e. VIC,TAS,NSW, etc
        * Description:  Populate Cultures by city pie chart module
        * Action:       Populate #myCulturesByCityPieChartContainer
        * Output:       None
        */
        populatePieChartCulturesByCity: function(term,state){

          console.log("I was called!");

            if (startDate === null && startDate === undefined){
              startDate = moment().subtract(29, 'days');
          
            }

            if (endDate ===null && endDate ===undefined){
              endDate = moment();
            }

            //Then Build the URL in order to send to the python service:
            var request = this.cultures_totals_by_city_service_url.concat(term + '/' + state + '/' + startDate + '/' + endDate); //date missing

            $.getJSON(request, function(data) {

              // console.log(data);

              var helper = new Helper();

              var title = "Population vs. Tweets in: " + $( "#select-cities option:selected" ).text();

              var dataChart = helper.getCultureTotalsByCityPieChartData(data,title);

              $('#myCulturesByCityPieChartContainer').highcharts(dataChart);


            });

          },

        /* 
        * Name:         populateSentimentTotalsByCity
        * Module:       Sentiment totals by city
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        *               state (String)  -> state code i.e. VIC,TAS,NSW, etc
        * Description:  Populate a line chart with sentiment results in order to check which culture is the most happiest
        *               and the most misserable (by a particular term or any term)
        * Action:       Populate #mySentimentByCityLineChartContainer
        * Output:       None
        */
        populateSentimentTotalsByCity: function(term,state){

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          //Then Build the URL in order to send to the python service:
          var request = this.sentiment_totals_by_city_service_url.concat(term + '/' + state + '/' + startDate + '/' + endDate); //date missing

          $.getJSON(request, function(data) {

            var helper = new Helper();
            var city = helper.getCityName(state);

            var dataChart = helper.getSentimentTotalsByCityLineChartData(data,"Sentiment Analysis by Suburb", city);

            $('#mySentimentByCityLineChartContainer').highcharts(dataChart);


          });

        },

        /* 
        * Name:         populatePopulationVsTweetsBarChart
        * Module:       Tweets vs. Population results
        * Parameters:   term (String)   -> Text you want to search for. i.e. AFL, Tony Abbott or * 
        * Description:  Populate a line chart for comparing the amount of tweets vs the actual population by suburb
        * Action:       Populate #myCulturesByCityBarChartContainer
        * Output:       None
        */
        populatePopulationVsTweetsBarChart: function(term){

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          var helper = new Helper();

          if (tableRecordsGlobal !== null && tableRecordsGlobal !== undefined){

            var title = "Cultures vs. Percentage of Tweets in: " + $( "#select-cities option:selected" ).text();

            var dataChart = helper.getPopulationVsTweetsBarChartData(tableRecordsGlobal,title,'Count');

            $('#myCulturesByCityBarChartContainer').highcharts(dataChart);

          }else{
            helper.errorMessage('Error Loading Population vs. Tweets Bar chart');
          }

        },

        /* CLustering topics */
        populateCluster: function(term){

          console.log("I'm the cluster!");
          var helper = new Helper();
          // var request = helper.getClusteredData(term,"text");

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(6, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          var request = {
                     "search_request":{
                      "query": {
                        "query_string": {
                          "query": "text:" + term + " AND created_at:[" + startDate + " TO " + endDate + "]"
                        }
                      },
                      },
                      "size": 10000,
                      "query_hint": term,
                            "field_mapping":{
                              "title": ["_source.title"],
                              "content": ["_source.text"]
                              },
                      "algorithm": "lingo",
                        "attributes": {
                            "LingoClusteringAlgorithm.desiredClusterCountBase": 5
                        },
                        "include_hits": true
                      };
          console.log(request);

          var getUrl = this.clustering_url+"?"
             + "q="+term+"&"
             + "size=5000&"
             + "field_mapping_title=_source.title&"
             + "field_mapping_content=_source.text&algorithm=lingo&include_hits=false";

          console.log(getUrl);
   
          $.ajax({
              url: getUrl,
              type: 'GET',
              contentType: 'application/json',
              crossDomain: true,
              dataType: 'json',
              data: JSON.stringify(request),
              success: function(response) {

                  var title = "Clustering";
                  var helper = Helper();
                  var foamTree=helper.getClusterData(response,title);
                  console.log("DONE");

              },
              error: function(jqXHR, textStatus, errorThrown) {
                  var jso = jQuery.parseJSON(jqXHR.responseText);
                  console.log( jqXHR.status + ':' + errorThrown + ':' + jso.error);
              }
          }); 
          console.log(JSON.stringify(request));
      }

    };
  };

  return PageModule;

});
