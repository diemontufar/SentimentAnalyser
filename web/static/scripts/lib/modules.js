/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       Here are defined the main modules: maps, chatrs and the tweeter feed.
 					  All their behaviour is managed through this script.
 * ======================================================================== */
/*global google */

define(["util/helper","qbuilder/qbuilder"], function(Helper,QBuilder)
{
  "use strict";
  var chart = document.getElementById('piechart_3d');
  var default_img_avatar = "../static/img/undefined.png";
  var qBuilder = new QBuilder();

  var PageModule = function()
  {
    return {

        search_service_url : '/customSearch/',
        geo_search_service_url : '/customGeoSearch/', //Gooood!
        sentiment_totals_service_url : '/sentimentTotals/',
        list_suburbs_service_url : '/listSuburbs/',
        cultures_service_url : '/culturesByCity',
        list_languages_service_url : '/languagesByCountry/',
        table_cultures_service_url : '/tweetsByCountryOfBirth/',
        custom_agg_service_url : '/customAggregation/',
        list_top_bysuburb_service_url: 'topListBySuburb/', //Good!

        initialize : function() {

        },

        /* Populate Top 5 Twitterers */
        populateTopTwitterers: function(term,suburb,size) { 

          var field = "user.screen_name";

          var request = this.list_top_bysuburb_service_url + term + '/' + suburb + '/' + field + '/' + size;

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
              helper.infoMessage('No Top twitterers found');
            }
            
            html_user += '</ol>';
            $('#toptwitterers-div').append(html_user);

          }).fail(function(){
            var helper = new Helper();
            helper.errorMessage('Error Loading Top Tweetterers');
          });

        },

        /* Populate Top 5 Trends */
        populateTopTrends: function(term,suburb,size) { 

          var field = "entities.hashtags.text";

          var request = this.list_top_bysuburb_service_url + term + '/' + suburb + '/' + field + '/' + size;

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
              helper.infoMessage('No Trends found');
            }
            
            html_user += '</ol>';
            $('#toptrends-div').append(html_user);

          }).fail(function(){
            var helper = new Helper();
            helper.errorMessage('Error Loading Top Trends');
          });

        },

        /* Populate Tweets using JSON files */
        populateTweetModuleByTerm: function(term,suburb,start,size) { 

          //Then Build the URL in order to send to the python service:
          var request = this.geo_search_service_url + term + '/' + suburb + '/' +  start + '/' + size;

          // Send JSON request
          // The returned JSON object will have a property called "results" where we find
          // a list of the tweets matching our request query
          $.getJSON(request, function(data) {

              if (data) {
                  $('#tab_1-1').empty();
                  $('#tab_2-2').empty();
                  $('#tab_3-3').empty();

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
                          }else if(sentiment_analysis.sentiment=='negative'){
                            $('#tab_3-3').append(tweet_html);
                          }else if(sentiment_analysis.sentiment=='neutral'){
                            $('#tab_2-2').append(tweet_html);
                          }
                        }
                    
                    }
                    
                });
              }

          }); //End getJSON

        },

        /* Get data from web services in order to populate pie chart*/
        populateChartModule : function(chart,term,suburb){

          //Then Build the URL in order to send to the python service:
          var request = this.sentiment_totals_service_url.concat(term + '/' + suburb);

          var pie_chart = chart;

          $.getJSON(request,function(data) {

                data = JSON.parse(data);
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

        /* Obtain list of Cities by state*/
        populateListOfCities : function(){

          var helper = new Helper();
          $('#select-suburbs').empty();
          $('#select-cities').empty();
          var country_code = "1"; //Australia

          $.getJSON(this.list_suburbs_service_url + country_code).done(function(data) {

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

        /* Obtain list of Countries fo birth in order to populate list boxes*/
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

        populateTable: function(term,state,suburb,date){

          //Then Build the URL in order to send to the python service:
          var request = this.table_cultures_service_url.concat(term + '/' + state + '/' + suburb); //date missing
          tableRecordsGlobal = null;

          $.getJSON(request, function(countryRecords) {

            // console.log(countryRecords);

            if (countryRecords){

              var helper = new Helper();
              var tableRecords = helper.getCulturesRecords(countryRecords);
              tableRecordsGlobal = tableRecords;
              tableRecordsGlobal = tableRecordsGlobal.sort(function(a,b) { return parseFloat(b.tweets) - parseFloat(a.tweets) } );

              //Populate Top 5 
               $('#topcountries-div').empty();
               var html_cultures = '<ol type="1">';
               var i = 0;
               $.each(tableRecordsGlobal,function(key,record){

                  if (i<5 && record.tweets != 0){
                    html_cultures += '<li><h5>' + record.countryOfBirth + '</h5></li>';
                    i++;
                  }

               });

               html_cultures += '</ol>';
               $('#topcountries-div').append(html_cultures);

              // console.log(tableRecords);
               var dynatable = $('#table-cultures').data('dynatable');
               dynatable.settings.dataset.originalRecords = tableRecords;
               dynatable.paginationPerPage.set(8);
               dynatable.process();

            }else{
              var suburb = $('#select-suburbs :selected').text();
              helper.infoMessage('Cultures table cannot be populated for: ' + suburb );
            }

          });

        },

        // populatePositivePeople: function(term,suburb){

        //   //First build the query for searching the term as follows:
        //   var qBuilder = new QBuilder();
        //   var query = qBuilder.buildTopAggregation(term,"positive",suburb);

        //   $('#positive-people-div h3').empty();
        //   $('#positive-people-div h4').empty();

        //   $.getJSON(this.custom_agg_service_url + query, function(data) {

        //     var countryCode = data["aggregations"]["2"]["buckets"][0]["key"];
        //     var count = data["aggregations"]["2"]["buckets"][0]["doc_count"];
        //     var helper = new Helper();
        //     var country = helper.getCountryName(countryCode);

        //     $('#positive-people-div h3').append(country);
        //     $('#positive-people-div h4').append(count);

        //   });

        // },

        // populateNegativePeople: function(term,suburb){

        //   //First build the query for searching the term as follows:
        //   var qBuilder = new QBuilder();
        //   var query = qBuilder.buildTopAggregation(term,"negative",suburb);

        //   $('#negative-people-div h3').empty();
        //   $('#negative-people-div h4').empty();

        //   $.getJSON(this.custom_agg_service_url + query, function(data) {

        //     var countryCode = data["aggregations"]["2"]["buckets"][0]["key"];
        //     var count = data["aggregations"]["2"]["buckets"][0]["doc_count"];
        //     var helper = new Helper();
        //     var country = helper.getCountryName(countryCode);

        //     $('#negative-people-div h3').append(country);
        //     $('#negative-people-div h4').append(count);

        //   });

        // },

        populateListOfLanguages: function(){

          $.getJSON(this.list_languages_service_url + '1', function(data) {

            languagesGlobal = data;

          });

        },

        /*Obtain tweets (only map markers) within a suburb*/ //Goooood!
        drawTweetsBySuburb : function(term,suburb){

          var startP = 0;
          var sizeP = 10000;

          //Then Build the URL in order to send to the python service:
          var request = this.geo_search_service_url + term + '/' + suburb + '/' + startP + '/' + sizeP;

          $.getJSON(request, function(data) {

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
                        
                    }else{
                      console.log("Undefined");
                    }

                  }); //inner inner each

              console.log(mapLanguages);
              console.log("Total retrieved tweets: " + total_retrieved_tweets);
              var helper = new Helper();
              setAllMap(map); //Add all markers to the map
              
              } //if data
          }); //End getJSON
      }


    };
  };

  return PageModule;

});
