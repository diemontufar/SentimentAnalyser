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
        geo_search_service_url : '/customGeoSearch/',
        sentiment_totals_service_url : '/sentimentTotals/',
        list_suburbs_service_url : '/listSuburbs',
        cultures_service_url : '/culturesByCity',

        initialize : function(chart) {

        },

        /* Populate Top 5 Twitterers */
        populateTopTwitterers: function(term,size) { 

          var field = "user.screen_name";
          //First build the query for searching the term as follows:
          var qBuilder = new QBuilder();
          var query = qBuilder.buildBasicAggregation(term,field,size);

          $.getJSON(this.search_service_url + query).done(function(data) {

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
        populateTopTrends: function(term,size) { 

          var field = "entities.hashtags.text";
          //First build the query for searching the term as follows:
          var qBuilder = new QBuilder();
          var query = qBuilder.buildBasicAggregation(term,field,size);

          $.getJSON(this.search_service_url + query).done(function(data) {

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
        populateTweetModuleByTerm: function(term,start,size) { 

          //First build the query for searching the term as follows:
          var query = qBuilder.buildPaginatedSearchByTerm(term,start,size);
          // console.log(query);
          //Then Build the URL in order to send to the python service:
          var request = this.search_service_url.concat(query);

          // Send JSON request
          // The returned JSON object will have a property called "results" where we find
          // a list of the tweets matching our request query
          $.getJSON(request, function(data) {

              

              if (data) {
                  $('#tab_1-1').empty();
                  $('#tab_2-2').empty();
                  $('#tab_3-3').empty();
                  // deleteMarkers();

                  $.each(data.hits, function(key, hits) {

                      if (hits) {

                          $.each(hits, function(j, sources) {

                              if (sources) {

                                  $.each(sources, function(i, tweet) {

                                      // console.log(tweet.text);
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

                                          // //console.log(helper.getGeoMarkerPoint(tweet));
                                          // var marker = helper.getGeoMarkerPoint(tweet);
                                          // addMarker(marker); //Add markers to the map and the markers array

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
                                          
                                      } //if tweet

                                  }); //inner inner each
                              } //if sources
                          }); //inner each 
                      } //if hits
                      else{
                        var helper = new Helper();
                        helper.infoMessage('No results found for topic: ' + term );
                      }
                  }); //outer each 
              // setAllMap(map); //Add all markers to the map
              } //if data
          }); //End getJSON

        },

        /* Get data from web services in order to populate pie chart*/
        populateChartModule : function(chart,term){

          //First build the query for searching the term as follows:
          var query = qBuilder.buildSearchByTerm(term);

          //Then Build the URL in order to send to the python service:
          var request = this.sentiment_totals_service_url.concat(query);

          
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

        /* Obtain list of Cities by state*/
        populateListOfCities : function(){

          var helper = new Helper();
          $('#select-suburbs').empty();
          $('#select-cities').empty();

          $.getJSON(this.list_suburbs_service_url).done(function(data) {

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

        /* Obtain list of Countries fo birth in order to populate table*/
        populateTableOfCultures : function(suburb){

          var table_html = '';
          var count = 1;
          var coutryRecords = [];

          if (cultures!==null && cultures!==undefined){

            $.each(cultures.features, function(fea, feature) {

                  if (feature.properties.feature_code ==  suburb){

                      $.each(feature.properties.country_of_birth, function(cou, country) {


                          coutryRecords[count-1] = {
                                                      'countryOfBirth' : country.name,
                                                      'males' : country.population.males,
                                                      'females' : country.population.females,
                                                      'total' : country.population.total,
                                                      'tweets' : 0
                                                    };

                          count++;

                      });

                     var dynatable = $('#table-cultures').data('dynatable');
                     dynatable.settings.dataset.originalRecords = coutryRecords;
                     dynatable.paginationPerPage.set(8);
                     dynatable.process();

                  }

            });

          }else{
            var helper = new Helper();
            var suburb = $('#select-suburbs :selected').text();
            helper.infoMessage('Cultures table cannot be populated for: ' + suburb );
          }

        },

        /*Obtain tweets (only map markers) within a suburb*/
        drawTweetsBySuburb : function(term,suburb){

          //Then Build the URL in order to send to the python service:
          var request = this.geo_search_service_url.concat(term + '/' + suburb);


          $.getJSON(request, function(data) {

            var mapLanguages = [];

              if (data) {

                  var helper = new Helper();
                  deleteMarkers();

                  $.each(data.hits, function(key, hits) {

                      if (hits) {

                          $.each(hits, function(j, sources) {

                              if (sources) {

                                  $.each(sources, function(i, tweet) {

                                      // Before we continue we check that we got data
                                      if (tweet.text !== undefined && tweet != null) {
                                          // Calculate how many hours ago was the tweet posted
                                          var date_tweet = new Date(tweet.created_at);
                                          var date_locale = date_tweet.format(' H:i:s - d M Y');

                                          mapLanguages[tweet.user.lang] = (mapLanguages[tweet.user.lang]||0)+1;
                                          // console.log(tweet.lang);
                                          // Build the html string for the current tweet
                                          //console.log(helper.getGeoMarkerPoint(tweet));
                                          var marker = helper.getGeoMarkerPoint(tweet);
                                          addMarker(marker); //Add markers to the map and the markers array
                                          
                                      } //if tweet

                                  }); //inner inner each
                              } //if sources
                          }); //inner each 
                      } //if hits
                      else{
                        helper.infoMessage('No results found for topic: ' + term );
                      }
                  }); //outer each 
              console.log(mapLanguages);
              setAllMap(map); //Add all markers to the map
              
              } //if data
          }); //End getJSON

      }

  
    };
  };

  return PageModule;

});
