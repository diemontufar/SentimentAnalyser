/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       Here are defined the main modules: maps, chatrs and the tweeter feed.
 					  All their behaviour is managed through this script.
 * ======================================================================== */
/*global google */

define(["util/helper","highcharts","exporting"], function(Helper,Highcharts,Exporting)
{
  "use strict";
  var chart = document.getElementById('piechart_3d');
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


        geo_search_service_url : '/genericGeoSearch/', 
        sentiment_totals_service_url : '/sentimentTotals/',
        table_cultures_service_url : '/tweetsByCountryOfBirth/',
        list_top_bysuburb_service_url: '/topListBySuburb/', 
        
        list_top_by_city_service_url: '/topListByCity/',
        cultures_totals_by_city_servide_url: '/cultureTotalsByCity/',
        sentiment_totals_by_city_service_url: '/sentimentTotalsByCity/',


        initialize : function() {

        },

        /* 
        * Name:         populateListOfCities
        * Module:       Cities list box
        * Parameters:   None
        * Description:  Obtain list of Cities by state from the suburbs database and filtering them by the states defined on the helper class   
        * Ation:        Populate #select-cities
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
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
        */
        populateListOfSuburbs : function(state){

          $('#select-suburbs').empty();
          cultures = null;

          $.getJSON(this.cultures_service_url+'/'+state).done(function(data) {

            if (data !== null && data!==undefined){

               var suburbs_options_html =  '<option value="all" disabled selected style="display:none;">Select a Suburb</option>';

               // console.log(data.state_coordinate);

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
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
        */
        populateListOfLanguages: function(){

          $.getJSON(this.languages_service_url + '1', function(data) {

            languagesGlobal = data;

          });

        },

        /* 
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
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

            var dataChart = helper.getTweetsByCityBarChartData(data,"Tweets by City","No. of Tweets");

            $('#mySentimentResultsByCityChartContainer').highcharts(dataChart);

          });

          
        },

      /* 
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
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

            var dataChart = helper.getTopTrendsByCityBarChartData(data,"#","Tweets by City","% of Tweets");

            $('#myTrendsByCityChartContainer').highcharts(dataChart);


          });

        },


        /* 
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
        */
        populateTopTwitterers: function(term,suburb,size) { 

          var field = "user.screen_name";

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          var request = this.list_top_bysuburb_service_url + term + '/' + suburb + '/' + field + '/' + size + '/' + startDate + '/' + endDate;

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
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
        */
        populateTopTrends: function(term,suburb,size) { 

          var field = "entities.hashtags.text";

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          var request = this.list_top_bysuburb_service_url + term + '/' + suburb + '/' + field + '/' + size + '/' + startDate + '/' + endDate;

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
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
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
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
        */
        populateChartModule : function(chart,term,suburb){

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          //Then Build the URL in order to send to the python service:
          var request = this.sentiment_totals_service_url.concat(term + '/' + suburb + '/' + startDate + '/' + endDate);

          var pie_chart = chart;

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
                     
                    pie_chart.drawPieChart(chart_results);
                    $('#label-showing').empty();
                    $('#label-showing').append('Showing from 1 to ' + size_page + ' of  ' + total_tweets + ' tweets');

                    $('#overall-sentiment-div h3').empty();
                    $('#overall-sentiment-div h3').append(result.mean_sentiment);

                    $('#total-tweets-div h3').empty();
                    $('#total-tweets-div h3').append(total_tweets);

                    var icon;
                    var color;
                    document.getElementById("overall-icon").className = "";
                    document.getElementById("overall-div").className = "";
                    
                    if (result.mean_sentiment == 'Positive'){
                      icon = "fa " + helper.sentiment_icon.positive;
                      color = "small-box bg-aqua";
                    }else if (result.mean_sentiment == 'Negative'){
                      icon = "fa " + helper.sentiment_icon.negative;
                      color = "small-box bg-red";
                    }else{
                      icon = "fa " + helper.sentiment_icon.neutral;
                      color = "small-box bg-green";
                    }

                    document.getElementById("overall-icon").className = icon;
                    document.getElementById("overall-div").className = color;
                   
                 });
              }

        	}); //End getJSON

        }, //end populateTableModule

        /* 
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
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
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
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
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
        */
      /* Caution: this takes too much time!! */
      populatePieChartCulturesByCity: function(term,state){

          if (startDate === null && startDate === undefined){
            startDate = moment().subtract(29, 'days');
        
          }

          if (endDate ===null && endDate ===undefined){
            endDate = moment();
          }

          //Then Build the URL in order to send to the python service:
          var request = this.cultures_totals_by_city_servide_url.concat(term + '/' + state + '/' + startDate + '/' + endDate); //date missing

          $.getJSON(request, function(data) {

            // console.log(data);

            var helper = new Helper();

            var title = $( "#select-cities option:selected" ).text();

            var dataChart = helper.getCultureTotalsByCityPieChartData(data,title);

            $('#myCulturesByCityPieChartContainer').highcharts(dataChart);


          });

        },

        /* 
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
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

            console.log(data);

            var helper = new Helper();
            var city = helper.getCityName(state);

            var dataChart = helper.getSentimentTotalsByCityLineChartData(data,"Sentiment Analysis by Suburb", city);

            $('#mySentimentByCityLineChartContainer').highcharts(dataChart);


          });

        },

         /* 
        * Name:         
        * Module:       
        * Parameters:   
        * Description:  
        * Ation:        
        * Output:       
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

            var title = $( "#select-cities option:selected" ).text();

            var dataChart = helper.getPopulationVsTweetsBarChartData(tableRecordsGlobal,title,'Count');

            $('#myCulturesByCityBarChartContainer').highcharts(dataChart);

          }else{
            helper.errorMessage('Error Loading Population vs. Tweets Bar chart');
          }

        }


    };
  };

  return PageModule;

});
