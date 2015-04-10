/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       Here are defined the main modules: maps, chatrs and the tweeter feed.
 					  All thir behaviour is managed through this script.
 * ======================================================================== */
/*global google */

define(["helper","qbuilder"], function(Helper,QBuilder)
{
  "use strict";
  var qBuilder = new QBuilder();
  var chart = document.getElementById('piechart_3d');
  var default_img_avatar = "../static/img/undefined.png"

  var PageModule = function()
  {
    return {

        twitter_api_url : 'http://localhost/test_json/tweetfeed',
        search_service_url : 'http://localhost/customSearch/',
        // results_url : 'http://localhost/test_json/pie',
        chart_table_service_url : 'http://localhost/chartTableSearch/',

        initialize : function(chart) {

        },

        /* Populate Tweets using JSON files */
        populateTweetModule : function(){

          // Send JSON request
          // The returned JSON object will have a property called "results" where we find
          // a list of the tweets matching our request query
          $.getJSON(this.twitter_api_url,function(data) {
              var helper = new Helper();

              $('#tab_1-1').empty();
              $('#tab_2-2').empty();
              $('#tab_3-3').empty();
              
              $.each(data.rows, function(key, rows) {
                // Uncomment line below to show tweet data in Fire Bug console
                // Very helpful to find out what is available in the tweet objects
                $.each(rows, function(i, tweet) {
        	        // Before we continue we check that we got data
        	        if(tweet.text !== undefined && tweet!=null) {
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
              				tweet_html	  += '<p class="message">';
              				tweet_html	  += '<a href="http://www.twitter.com/' + tweet.user.screen_name + '" class="name">';
              				tweet_html	  += '<small class="text-muted pull-right"><i class="fa fa-clock-o"><\/i>' + date_locale + '<\/small>';
              				tweet_html	  += tweet.user.name + '<\/a>';
              				tweet_html	  += '<small class="text-muted">' + '@' + tweet.user.screen_name + '<\/small><br>';
              				tweet_html	  += tweet_text;
              				tweet_html	  += '<\/p><div class="attachment">';
              				tweet_html	  += '<small class="text-muted">Retweets: ' + tweet.retweet_count + ' | Favorites: ' + tweet.favorite_count + ' | Sentiment: <i class="fa ' + icon + '"><\/i><\/small>';
              				tweet_html	  += '<\/div><\/div>';

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
        	   });
            });

        },

        /* Populate Tweets using JSON files */
        populateTweetModuleByTerm: function(term) { 

          //First build the query for searching the term as follows:
          var query = qBuilder.buildSearchByTerm(term);
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
                                          
                                      } //if tweet

                                  }); //inner inner each
                              } //if sources
                          }); //inner each 
                      } //if hits
                  }); //outer each 
              } //if data
          }); //End getJSON

        },

        /* Parse results.json file and present data on modules*/
        populateTableModule : function(chart,term){

          //First build the query for searching the term as follows:
          var query = qBuilder.buildSearchByTerm(term);
          //Then Build the URL in order to send to the python service:
          var request = this.chart_table_service_url.concat(query);

          var table_html = '<tr><th>State/Territory<\/th><th>Sentiment<\/th><th>Positive<\/th><th>Neutral<\/th><th>Negative<\/th><\/tr>';
          var helper = new Helper();
          var pie_chart = chart;

          $.getJSON(request,function(data) {

                data = JSON.parse(data);

                if (data !== undefined && data !== null){

                  $('#regions-table').empty();

                  $.each(data, function(res, result) {

                		$.each(result.regions, function(reg, region) {

          		        table_html += '<tr>';
          		        table_html += '<td><a href="#">' + region.name +'<\/a><\/td>';
          		        table_html += '<td>' + '<i class="fa ' + helper.sentiment_icon[region.sentiment] + '"><\/i><\/td>';
          		        table_html += '<td>' + region.positive +'<\/td>';
          		        table_html += '<td>' + region.neutral +'<\/td>';
          		        table_html += '<td>' + region.negative +'<\/td>';
          		        table_html +=  '<\/tr>';

                		});

                    var chart_results = google.visualization.arrayToDataTable([
                      ['Results', 'Totals per Sentiment'],
                      ['Positive',  parseInt(result.total_positive)],
                      ['Negative',  parseInt(result.total_negative)],
                      ['Neutral',   parseInt(result.total_neutral)]
                    ]);
                     
                    pie_chart.drawPieChart(chart_results);
                   
                 });
              }

               // Append html string to results table
        	    $('#regions-table').append(table_html);
        	}); //End getJSON

        } //end populateTableModule
  
    };
  };

  return PageModule;

});
