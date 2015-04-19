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

        search_service_url : 'http://localhost/customSearch/',
        sentiment_totals_service_url : 'http://localhost/sentimentTotals/',
        list_suburbs_service_url : 'http://localhost/listSuburbs',
        cultures_service_url : 'http://localhost/culturesByCity',

        initialize : function(chart) {

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

              var helper = new Helper();

              if (data) {
                  $('#tab_1-1').empty();
                  $('#tab_2-2').empty();
                  $('#tab_3-3').empty();
                  deleteMarkers();

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

                                          //console.log(helper.getGeoMarkerPoint(tweet));
                                          var marker = helper.getGeoMarkerPoint(tweet);
                                          addMarker(marker); //Add markers to the map and the markers array

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
                  }); //outer each 
              setAllMap(map); //Add all markers to the map
              } //if data
          }); //End getJSON

        },

        /* Get data from web services in order to populate pie chart*/
        populateChartModule : function(chart,term){

          //First build the query for searching the term as follows:
          var query = qBuilder.buildSearchByTerm(term);
          // console.log(query);
          //Then Build the URL in order to send to the python service:
          var request = this.sentiment_totals_service_url.concat(query);

          // var table_html = '<tr><th>State/Territory<\/th><th>Sentiment<\/th><th>Positive<\/th><th>Neutral<\/th><th>Negative<\/th><\/tr>';
          var helper = new Helper();
          var pie_chart = chart;

          $.getJSON(request,function(data) {

                data = JSON.parse(data);

                if (data !== undefined && data !== null){

                  // $('#regions-table').empty();

                  $.each(data, function(res, result) {

                		// $.each(result.regions, function(reg, region) {

          		      //   table_html += '<tr>';
          		      //   table_html += '<td><a href="#">' + region.name +'<\/a><\/td>';
          		      //   table_html += '<td>' + '<i class="fa ' + helper.sentiment_icon[region.sentiment] + '"><\/i><\/td>';
          		      //   table_html += '<td>' + region.positive +'<\/td>';
          		      //   table_html += '<td>' + region.neutral +'<\/td>';
          		      //   table_html += '<td>' + region.negative +'<\/td>';
          		      //   table_html +=  '<\/tr>';

                		// });

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
                   
                 });
              }

               // Append html string to results table
        	    // $('#regions-table').append(table_html);
        	}); //End getJSON

        }, //end populateTableModule

        /* Obtain list of Countries fo birth in order to populate list boxes*/
        populateListOfSuburbs : function(state){

          $('#select-suburbs').empty();
          // console.log(city);

          $.getJSON(this.cultures_service_url+'/'+state,function(data) {


            if (data !== null && data!==undefined){

               var suburbs_options_html =  '<option value="all" disabled selected style="display:none;">Suburbs</option>';

               // console.log(data.state_coordinate);

               var lat = data.crs.properties.state_coordinate[0];
               var lang = data.crs.properties.state_coordinate[1];
               var zoom = data.crs.properties.state_coordinate[2];

               $.each(data.features, function(fea, feature) {

                  suburbs_options_html = suburbs_options_html + '<option value="' + feature.properties.feature_code + '">' + feature.properties.feature_name + '</option>';

               });


              // var geoJson = JSON.parse(data);
              // console.log(data);
              map.data.addGeoJson(data);

              map.setCenter(new google.maps.LatLng(lat, lang));
              map.setZoom(zoom);
               // Append html string to suburb option list
              $('#select-suburbs').append(suburbs_options_html);

            }
          });

        },

        /* Obtain list of Countries fo birth in order to populate list boxes*/
        populateListOfCities : function(){

          $.getJSON(this.list_suburbs_service_url,function(data) {

            var city_options_html =  '<option value="all" disabled selected style="display:none;">Main Cities</option>';

              $.each(data.states, function(sta, state) {

                if (isInStateList(state.state)){

                  // if (state.state=='VIC') //Set Melbourne as default
                  //   city_options_html = city_options_html + '<option selected value="' + state.state + '">' + getCityName(state.state) + '</option>';
                  // else
                    city_options_html = city_options_html + '<option value="' + state.state + '">' + getCityName(state.state) + '</option>';

                }

              });
               // Append html string to cities option list
              $('#select-cities').append(city_options_html);

          });

        }

  
    };
  };

  return PageModule;

});
