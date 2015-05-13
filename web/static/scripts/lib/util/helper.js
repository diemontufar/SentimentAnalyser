/* ========================================================================
 * Author:            Diego Montufar
 * Date:              Feb/2015
 * Description:       Helper class is used to perform non-trivial tasks such as:
 						- Configuring date and time parameters
 						- Parsing texts, links, emails, etc.
 						- Getting goe positioning data and computing coordinate points for GMaps 
 						- Reseting global variables, modules and other values
 						- Building configuration structures in order to populate chart modules
 * ======================================================================== */

//Define a global list of relevant states and names of Australia
var statesList = {};
	statesList['VIC'] = 'Melbourne';
	statesList['NSW'] = 'Sydney';
	statesList['TAS'] = 'Hobart';
	statesList['QLD'] = 'Brisbane';
	statesList['NT'] = 'Darwin';
	statesList['WA'] = 'Perth';
	statesList['SA'] = 'Adelaide';

function calculateUniqueDocumentsCount(cluster) {
  var uniqueIds = {};
  if (cluster.documents) {
    cluster.documents.forEach(function(id) {
      uniqueIds[id] = true;
    });
  }
  
  if (cluster.clusters) {
    cluster.clusters.forEach(function(subcluster) {
      for (var key in calculateUniqueDocumentsCount(subcluster)) {
        uniqueIds[key] = true;
      };
    });
  }
  cluster.uniqueDocumentsCount = Object.keys(uniqueIds).length;
  return uniqueIds;
};

define(["moment"], function(Moment)
{
	"use strict";

	/* Class Helper */
	var Helper = function()
	{
		return {

			sentiment_icon : {positive:"fa-thumbs-o-up",negative:"fa-thumbs-o-down",neutral:"fa-meh-o"},

			date_options : {
					drops:'up',
                    startDate: moment().subtract(6, 'days'),
                    endDate: moment(),
                    minDate: '01/01/2012',
                    maxDate: '12/31/2015',
                    dateLimit: { days: 120 },
                    showDropdowns: true,
                    showWeekNumbers: true,
                    timePicker: false,
                    timePickerIncrement: 1,
                    timePicker12Hour: true,
                    ranges: {
                       'Today': [moment(), moment()],
                       'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                       'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                       'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                       'This Month': [moment().startOf('month'), moment().endOf('month')],
                       'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                    },
                    opens: 'left',
                    format: 'MM/DD/YYYY',
                    separator: ' to ',
                    locale: {
                        applyLabel: 'Apply',
                        cancelLabel: 'Cancel',
                        fromLabel: 'From',
                        toLabel: 'To',
                        customRangeLabel: 'Custom',
                        daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr','Sa'],
                        monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                        firstDay: 1
                    }
             },

			/* Change text hyperlinks into real html links */
			parseLinks:function(tweet){
				return tweet.replace(/[A-Za-z]+:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&\?\/.=]+/g, function (tweet) {
			        return tweet.link(tweet);
			    });
			},

			/* Convert text into hashtags */
			parseHashTags:function(tweet){
				 return tweet.replace(/(^|\s)(#[a-z\d-]+)/ig, function (tweet) {
			        return tweet.link(tweet);
			    });
			},

			/* Recognize @ as a user in text */
			parseUser:function(tweet){
				return tweet.replace(/[@]+[A-Za-z0-9-_]+/g, function(u) {
					var username = u.replace('@','');
					return u.link("http://twitter.com/"+username);
				});
			},

			/* Build table structure based on records obtained from an elasticsearch response */
			getCulturesRecords:function(countryRecords){

			  var count = 1;
          	  var coutryRecordsResponse = [];

	          if (countryRecords!==null && countryRecords!==undefined ){

	            	$.each(countryRecords, function(cob, country) {

	                    coutryRecordsResponse[count-1] = {
	                                                'countryCode' : country.id,
	                                                'countryOfBirth' : country.name,
	                                                'countryLanguages' : country.languages,
	                                                'males' : country.population.males,
	                                                'females' : country.population.females,
	                                                'totalPopulation' : country.population.total,
	                                                'tweets' : country.count
	                                              };

	                    count++;

	                 });
				}//end if
				else{
					console.log("Cultures or languagesGlobal global variables are not defined!");
					coutryRecordsResponse =  undefined;
				}

				return coutryRecordsResponse;

			},

			/* Get the country name based on the language code */
			getCountryName:function(languageCode){

				var name;

				if (languagesGlobal!== null && languagesGlobal!==undefined){

					$.each(languagesGlobal.country_of_birth,function(key,country){

						$.each(country.languages,function(lan,language){
							if (language == languageCode.toLowerCase()){
								name = country.name;
								return;
							}
						});
					});

				}else{
					console.log("languagesGlobal is not defined!");
					name = null;
				}

				return name;

			},

			/* Compute the geo location of a tweet based on the coordinates/place fields */
			//Try to find a point whether it is defined on the coordinates field or in the place.bounding_box field.
			//When a bounding bos is found, we compute the central point which will serve as an estimate of the exact location.
			getGeoMarkerPoint: function(tweet){

			  var image = {url: '../static/img/marker-neutral.png', size: new google.maps.Size(32, 32)};

			  var sentiment_analysis = tweet.sentiment_analysis;
			  if (sentiment_analysis != null && sentiment_analysis != undefined){
				  if (tweet.sentiment_analysis.sentiment == 'positive'){
				  		image = {url: '../static/img/marker-positive.png', size: new google.maps.Size(32, 32)};
				  }else if (tweet.sentiment_analysis.sentiment == 'negative'){
				  		image = {url: '../static/img/marker-negative.png', size: new google.maps.Size(32, 32)};
				  }else{
				  		image = {url: '../static/img/marker-neutral.png', size: new google.maps.Size(32, 32)};
				  }
			  }

		      //If I cannot find point, search in coordinates
		      if (tweet.coordinates === null || tweet.coordinates === undefined){ 
		        //If I cannot find point, search in place.bounding_box.coordinates
		        if(tweet.coordinates === null || tweet.coordinates === undefined){
					//I'm gonna find the point for sure here
					var coord = tweet.place.bounding_box.coordinates[0];

					var bounds = new google.maps.LatLngBounds();
					var i;

					// The Bermuda Triangle
					var polygonCoords = [
						new google.maps.LatLng(coord[0][1], coord[0][0]),
						new google.maps.LatLng(coord[1][1], coord[1][0]),
						new google.maps.LatLng(coord[2][1], coord[2][0]),
						new google.maps.LatLng(coord[3][1], coord[3][0])
					];

					for (i = 0; i < polygonCoords.length; i++) {
						bounds.extend(polygonCoords[i]);
					}
					var point = bounds.getCenter();

					var marker = new google.maps.Marker({
											position: point,
											visible: true,
											icon: image
										});
		          return marker;
		        }else{ //calculate center point of bounding box
		          var coord = tweet.coordinates[0];
		          var bounds = new google.maps.LatLngBounds();
					var i;

					// The Bermuda Triangle
					var polygonCoords = [
						new google.maps.LatLng(coord[0][1], coord[0][0]),
						new google.maps.LatLng(coord[1][1], coord[1][0]),
						new google.maps.LatLng(coord[2][1], coord[2][0]),
						new google.maps.LatLng(coord[3][1], coord[3][0])
					];

					for (i = 0; i < polygonCoords.length; i++) {
						bounds.extend(polygonCoords[i]);
					}
					var point = bounds.getCenter();

					var marker = new google.maps.Marker({
											position: point,
											visible: true,
											icon: image
										});
		          return marker;
		        }
		      }else{
		      	var point = new google.maps.LatLng(tweet.geo.coordinates[0],tweet.geo.coordinates[1]);
	            var marker = new google.maps.Marker({
				    position: point,
				    visible: true,
				    icon: image
				});
		        return marker; //Found a coordinate
		      }

		  	},

		  	/* 
		  	* Method: 	   getTweetsByCityBarChartData
		  	* Description: Bar chart configuration structure
		  	* Module: 	   modules.populateSentimentByCityBarChart
		  	*/
            getTweetsByCityBarChartData: function(data,title,yAxisLabel){

            	  if (data !== undefined && data !== null){

            	  	var positives = [];
            	  	var negatives = [];
            	  	var neutrals = [];
            	  	var labelsStates = [];

            	  	$.each(data,function(key,value){

            	  		labelsStates.push(statesList[key]);
        	  			positives.push(value.positive);
	        	  		negatives.push(value.negative);
	        	  		neutrals.push(value.neutral);
            	  	});

		            var dataChart =	{
			              chart: {type: 'column'}, 
			              credits: {enabled: false }, 
			              exporting: {enabled: true }, 
			              title: {text: title }, 
			              xAxis: {categories: labelsStates }, 
			              yAxis: {title: {text: yAxisLabel } }, 
			              plotOptions: {
					            column: {
					                dataLabels: {
					                    enabled: true,
						                rotation: -90,
						                color: '#FFFFFF',
						                align: 'right',
						                y: -10, // 10 pixels down from the top
						                style: {
						                    fontSize: '9px',
						                    fontFamily: 'Verdana, sans-serif'
						                }
					                }
					            }
					        },
					      	lang: {
					            noData: "No results found"
					        },
					        noData: {
					            style: {
					                fontWeight: 'bold',
					                fontSize: '15px',
					                color: '#303030'
					            }
					        },
			              series: [{
			                  name: 'Positive',
			                  data: positives,
			                  color: '#00aff0',
			                  pointWidth: 20
			              }, 
			              {
			                  name: 'Negative',
			                  data: negatives,
			                  color: '#f05032',
			                  pointWidth: 20
			              },
			              {
			                  name: 'Neutral',
			                  data: neutrals,
			                  color: '#54b847',
			                  pointWidth: 20
			              }]
		          	};

			      }else{
			      	return undefined;
			      }

			      return dataChart;

            },

            /* 
		  	* Method: 	   getTopTrendsByCityBarChartData
		  	* Description: Bar chart configuration structure
		  	* Module: 	   modules.populateTopTrendsByCityBarChart
		  	*/
            getTopTrendsByCityBarChartData: function(data,type,title,yAxisLabel){

            	  if (data !== undefined && data !== null){

         			var colorList = ['#4572A7', '#AA4643', '#89A54E', '#80699B', '#3D96AE'];
            	  	var labelsStates = [];
            	  	var seriesP = [];

            	  	var countTop = 0;
            	  	var defaultP = [];

            	  	$.each(data,function(key,value){

            	  		var dataP = [];

            	  		$.each(value.buckets,function(hashtag,count){

	            	  		var dataT ={name: type + hashtag, data: [[countTop,count]] };
							dataP.push(dataT);
							
						});

            	  		if (dataP ===undefined || dataP ===null || dataP.length == 0){

            	  			// labelsStates.push(null);

            	  		}else{
            	  			for (var i=0;i<5;i++){
            	  				if (dataP[i]!==null && dataP[i]!=undefined){
            	  					seriesP.push(dataP[i]);
            	  				}
            	  			} 
            	  			labelsStates.push(statesList[key]);
            	  			countTop++;
            	  		}
            	  	});

            	  	// console.log(JSON.stringify(seriesP));

	            	  var dataChart = {
							        chart: {type: 'column'}, 
							        credits: {enabled: false }, 
							        title: {text: title }, 
							        exporting: {enabled: true }, 
							        xAxis: {categories: labelsStates },
							        yAxis: {
							            min: 0, title: {text: yAxisLabel }, 
							            stackLabels: {
							                enabled: true,
							                style: {
							                    fontWeight: 'bold',
							                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
							                }
							            }
							        },
							        tooltip: {
							                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.percentage:.0f}%)<br/>',
							                shared: true
							            },
							        plotOptions: {
							            column: {
							                stacking: 'percent',
							                dataLabels: {
							                    enabled: true,
							                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
							                    style: {
							                        textShadow: '0 0 3px black'
							                    }
							                }
							            }
							        },
							        legend: {
										align: 'right',
										borderWidth: 0,
										layout: 'vertical',
										itemMarginTop: 7,
										itemMarginBottom: 7,
										itemStyle: {
											lineHeight: '25px',
											fontFamily: "'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif",
											fontSize: '14px',
											color: '#333'
										},

										verticalAlign: 'top',
										x: -60,
										y: 110
									},
									labelFormatter: function () {
										// console.log(this);
							            // if (this.x == 0) return '<h2>{}</h2>' + this.name;
							            // else if (this.x == 2) return '<div class="second"><h2>Title Group 2</h2>' + this.name + '</div>';
							            // else return this.name;

							        },
							        lang: {
					            		noData: "No results found"
							        },
							        noData: {
							            style: {
							                fontWeight: 'bold',
							                fontSize: '15px',
							                color: '#303030'
							            }
							        },
							        "series": seriesP
							};

			      }else{
			      	return undefined;
			      }

			      return dataChart;

            },

            /* 
		  	* Method: 	   getCultureTotalsByCityPieChartData
		  	* Description: Pie chart configuration structure
		  	* Module: 	   modules.populatePieChartCulturesByCity
		  	*/
            getCultureTotalsByCityPieChartData: function(data,title){

            	  if (data !== undefined && data !== null){

            	  	var dataList = [];

            	  	$.each(data.buckets,function(key,value){

            	  		dataList.push([key,value]);

            	  	});

            	  	console.log(dataList);

		            var dataChart =	{
							        chart: {
							            plotBackgroundColor: null,
							            plotBorderWidth: null,
							            plotShadow: false
							        },
							        title: {
							            text: title
							        },
							        credits: {
									      enabled: false
									  },
							        tooltip: {
							            pointFormat: '{series.name}: <b>{point.y}</b>'
							        },
							        exporting: {
									  	enabled: true
									  },
							        plotOptions: {
							            pie: {
							                allowPointSelect: true,
							                cursor: 'pointer',
							                dataLabels: {
							                    enabled: true,
							                    format: '<b>{point.name}</b>: {point.percentage:.2f} %',
							                    style: {
							                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
							                    }
							                },
							                showInLegend: true
							            }
							        },
							        lang: {
					            		noData: "No results found"
							        },
							        noData: {
							            style: {
							                fontWeight: 'bold',
							                fontSize: '15px',
							                color: '#303030'
							            }
							        },
							        series: [{
							            type: 'pie',
							            name: 'No. of Tweets',
							            data: dataList
							        }]
							    };

			      }else{
			      	return undefined;
			      }

			      return dataChart;
            },

            /* 
		  	* Method: 	   getSentimentTotalsByCityLineChartData
		  	* Description: Line chart configuration structure
		  	* Module: 	   modules.populateSentimentTotalsByCity
		  	*/
            getSentimentTotalsByCityLineChartData: function(data,title,city){

            	  if (data !== undefined && data !== null){

            	  	var categoryList = [];
            	  	var positiveList = [];
            	  	var negativeList = [];
            	  	var neutralList = [];

            	  	$.each(data,function(key,value){

            	  		categoryList.push(value.suburb_name);
            	  		positiveList.push(value.results.total_positive);
            	  		negativeList.push(value.results.total_negative);
						neutralList.push(value.results.total_neutral);
            	  		

            	  	});

		            var dataChart =	{
							        chart: {type: 'line'}, 
							        title: {text: title }, 
							        subtitle: {
							            text: 'Looking at the most Happiest and Misserable suburb in: ' + city
							        },
							        credits: {enabled: false }, 
							        tooltip: {
										    crosshairs: true,
										    animation: true,
										    shared: true,
										    formatter: function() {
										        var html = '<b>' + this.x + '</b><br>';

										    	for (var i=0;i<this.points.length;i++){
										    		if (i !=  this.points.length - 1){
										    			html += '<b>' + this.points[i].series.name + '</b>: ' + this.points[i].y + '<br>';
										    		}else{
										    			html += '<b>' + this.points[i].series.name + '</b>: ' + this.points[i].y;
										    		}
										    	}
										    	return html;
										     }
										},
							        xAxis: {
							            categories: categoryList
							        },
							        yAxis: {
							            title: {
							                text: 'Sentiment count'
							            },
							            min: 0
							        },
							        plotOptions: {
							            line: {
							                dataLabels: {
							                    enabled: true
							                },
							                enableMouseTracking: true
							            }
							        },
							        lang: {
					            		noData: "No results found"
							        },
							        noData: {
							            style: {
							                fontWeight: 'bold',
							                fontSize: '15px',
							                color: '#303030'
							            }
							        },
							        series: [{
							            name: 'Positive',
							            data: positiveList,
							            color: '#00aff0'
							        }, {
							            name: 'Negative',
							            data: negativeList,
							            color: '#f05032'
							        },{
							            name: 'Neutral',
							            data: neutralList,
							            color: '#54b847'
							        }]
							    };

			      }else{
			      	return undefined;
			      }

			      return dataChart;
            },

            /* 
		  	* Method: 	   getPopulationVsTweetsBarChartData
		  	* Description: Bar chart configuration structure
		  	* Module: 	   modules.populatePopulationVsTweetsBarChart
		  	*/
            getPopulationVsTweetsBarChartData: function(data,title,yAxisLabel){

            	if (data !== undefined && data !== null){

            	  	var cultures = [];
            	  	var population = [];
            	  	var tweets = [];

            	  	$.each(data,function(key,value){

            	  		cultures.push(value.countryOfBirth);
        	  			population.push(value.totalPopulation);
            	  		tweets.push(value.tweets);

            	  	});

		            var dataChart =	{
			              chart: {zoomType: 'xy'}, 
			              credits: {enabled: false }, 
			              exporting: {enabled: true }, 
			              title: {text: title }, 
			              xAxis: {categories: cultures }, 
			              yAxis: [{ // Primary yAxis
						            labels: {
						                format: '{value}',
						                style: {
						                    color: Highcharts.getOptions().colors[1]
						                }
						            },
						            title: {
						                text: 'Population',
						                style: {
						                    color: Highcharts.getOptions().colors[1]
						                }
						            },
						            min: 0
						        }, { // Secondary yAxis
						            title: {
						                text: 'Tweets',
						                style: {
						                    color: Highcharts.getOptions().colors[0]
						                }
						            },
						            labels: {
						                format: '{value}',
						                style: {
						                    color: Highcharts.getOptions().colors[0]
						                }
						            },
						            min: 0,
						            opposite: true
						        }],
					        plotOptions: {
					            line: {
					                dataLabels: {
					                    enabled: true
					                },
					                enableMouseTracking: true
					            }
					        },
					      tooltip: {
						    crosshairs: true,
						    animation: true,
						    shared: true,
						    formatter: function() {
						    	var html = '<b>' + this.x + '</b><br>';

						    	for (var i=0;i<this.points.length;i++){
						    		if (i !=  this.points.length - 1){
						    			html += '<b>' + this.points[i].series.name + '</b>: ' + this.points[i].y + '<br>';
						    		}else{
						    			html += '<b>' + this.points[i].series.name + '</b>: ' + this.points[i].y;
						    		}
						    	}
						    	return html;
						    }
							},
							lang: {
					            noData: "No results found"
					        },
					        noData: {
					            style: {
					                fontWeight: 'bold',
					                fontSize: '15px',
					                color: '#303030'
					            }
					        },
							series: [{
					            name: 'No. of Tweets',
					            type: 'line',
					            yAxis: 1,
					            data: tweets
					        }, {
					            name: 'Population',
					            type: 'line',
					            data: population
					        }]
		          	};

			      }else{
			      	return undefined;
			      }

			      return dataChart;

            },

            getClusterData: function(response,title){

			      if (response !== undefined && response !== null){

			          if (response.hits.total > 0) {
			             $('#cluster').text("");
			          } else {
			             $('#cluster').text("no results found");
			          }

			          response.clusters.forEach(function(cluster) {
			             calculateUniqueDocumentsCount(cluster);
			          });

			          var visualizationInput = {
			             groups: response.clusters.map(function mapper(cluster) {
			                return {
			                   label: cluster.phrases[0],
			                   weight: cluster.uniqueDocumentsCount,
			                   groups: (cluster.clusters || []).map(mapper)
			                 }
			              })
			            };
			          if (typeof foamtree !== 'undefined'){
			                foamtree.dispose();
			          }
			          foamtree = new CarrotSearchFoamTree({
			             id: "cluster",
			             backgroundColor: "#fff",
			             dataObject: visualizationInput
			          });
         
			          console.log(visualizationInput);
			      }else{
			        return undefined;
			      }

			},

            getChartModuleData: function(response,title){

            	var data = response.results;
            	var colors = ['#00aff0', '#f05032', '#54b847'];

            	if (data !== undefined && data !== null){

            		var seriesP = [];


            		if (data.mean_sentiment == "Positive"){
            			seriesP.push({ name : "Positive", y: data.total_positive, sliced: true, selected: true , color: colors[0]}); 
            			seriesP.push({ name : "Negative", y: data.total_negative, color: colors[1] });
            			seriesP.push({ name : "Neutral", y: data.total_neutral, color: colors[2] });
            		}else if (data.mean_sentiment == "Negative"){
            			seriesP.push({ name : "Positive", y: data.total_positive, color: colors[0] });
            			seriesP.push({ name : "Negative", y: data.total_negative, sliced: true, selected: true, color: colors[1] });
            			seriesP.push({ name : "Neutral", y: data.total_neutral, color: colors[2] });
            		}else{
            			seriesP.push({ name : "Positive", y: data.total_positive, color: colors[0] });
            			seriesP.push({ name : "Negative", y: data.total_negative, color: colors[1] });
            			seriesP.push({ name : "Neutral", y: data.total_neutral, sliced: true, selected: true, color: colors[2] });
            		}

            		console.log(response);

            	var dataChart = {
						        chart: {
						            type: 'pie',
						            options3d: {
						                enabled: true,
						                alpha: 45,
						                beta: 0
						            },
						            events: {
						                load: function(event) {
						                	  var txt = '<b>Tweets</b><br>' + data.total_tweets;
						                      var label = this['renderer']['label'](txt)
						                   .css({
						                       'width': '150px',
						                       'color' : 'grey',
						                       'fontSize':'20px'
						                       
						                   })
						                   .attr({
						                       'stroke': 'grey',
						                       'stroke-width': 0,
						                       'r': 5,
						                       'padding': 3                      
						                   })
						                   .add();
						                   
						                   label.align(Highcharts.extend(['label']['getBBox()'], {
						                       'align': 'right',
						                       'x': -110, // offset
						                       'verticalAlign': 'bottom',
						                       'y': -150 // offset
						                   }), null, 'spacingBox');
						                }
						            }
						        },
						        credits: {enabled: false }, 
			              		exporting: {enabled: true }, 
						        title: {
						            text: title
						        },
						        tooltip: {
						            pointFormat: '{series.name}: <b>{point.y}</b>'
						        },
						        plotOptions: {
						            pie: {
						                allowPointSelect: true,
						                cursor: 'pointer',
						                dataLabels: {
						                    enabled: true,
						                    format: '<b>{point.name}</b>: {point.percentage:.2f} %',
						                    style: {
						                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
						                    }
						                },
						                showInLegend: true
						            }
						        },
						        lang: {
				            		noData: "No results found"
						        },
						        noData: {
						            style: {
						                fontWeight: 'bold',
						                fontSize: '15px',
						                color: '#303030'
						            }
						        },
						        series: [{
						            type: 'pie',
						            name: 'Tweets',
						            data: seriesP
						        }]
						    };
				}else{
			      	return undefined;
			      }

			      return dataChart;

            },

            // Clear and reset modules and global variables */
            restartModules: function(){

            	total_tweets = 0; //global variable for totals
            	cultures = null;
		        start_page = 0; //global variable for pagination
		        size_page = 50; //global variables for pagination
		        var fading_time = 2000;

		        $('#toptwitterers-div').empty();
		        $('#toptrends-div').empty();
		        $('#label-showing').empty();
		        $('#topcountries-div').empty();


		        $('#tab_1-1').empty();
		        $('#tab_2-2').empty();
		        $('#tab_3-3').empty();

		        $('#overall-sentiment-div h3').empty();
		        $('#overall-sentiment-div h3').append('None');

		        $('#total-tweets-div h3').empty();
		        $('#total-tweets-div h3').append('0');
		        
		        $('#section-piechart-cultures').fadeOut(2000);
		        $('#section-linechart-cultures').fadeOut(2000);

		        //Disclaimer messages
		        $('#disclaimer-sentiment').fadeOut(2000);
		        $('#disclaimer-trends').fadeOut(2000);

		        $("#section-feed").fadeOut(2000);
		        $("#section-toptwitterers").fadeOut(2000);
		        $("#section-toptrends").fadeOut(2000);
		        $("#section-topcountries").fadeOut(2000);
		        $("#div-totals").fadeOut(2000);
		        $('#section-chart').fadeOut(2000);

		    },

		    /* Check if state is in the states list */
		  	isInStateList: function(state){

				return statesList[state] != undefined;

		  	},

		  	/* Get the city name given the id */
		  	getCityName: function(id){
			  
			  return statesList[id];

			},

			/* Obtain date range string */
			getDateRange: function(start,end){

				var result = start.format('MMM D, YYYY') + " - " + end.format('MMM D, YYYY');

				var ranges = {
                       'Today': [moment().format('YYYY-MMMM-D'), moment().format('YYYY-MMMM-D')],
                       'Yesterday': [moment().subtract(1, 'days').format('YYYY-MMMM-D'), moment().subtract(1, 'days').format('YYYY-MMMM-D')],
                       'Last 7 Days': [moment().subtract(6, 'days').format('YYYY-MMMM-D'), moment().format('YYYY-MMMM-D')],
                       'Last 30 Days': [moment().subtract(29, 'days').format('YYYY-MMMM-D'), moment().format('YYYY-MMMM-D')],
                       'This Month': [moment().startOf('month').format('YYYY-MMMM-D'), moment().endOf('month').format('YYYY-MMMM-D')],
                       'Last Month': [moment().subtract(1, 'month').startOf('month').format('YYYY-MMMM-D'), moment().subtract(1, 'month').endOf('month').format('YYYY-MMMM-D')]
                    }

                $.each(ranges,function(rangeName,range){

                	if (start.format('YYYY-MMMM-D') == range[0] && end.format('YYYY-MMMM-D') == range[1]){
                		result = rangeName;
                	}

                });

                return result;

			},

			/* Configure message modal window for info */
			infoMessage: function(msg){
		        var icon = '<i class="icon fa fa-info" style="margin-right: 10px;"></i>';
		        $('.modal-title').empty();
		        $('.modal-body').empty();
		        $('.modal-title').append(icon+'Info');
		        $('.modal-body').append(msg);
		        $('#basicModal').modal('show');
		    },

		    /* Configure message modal window for alert */
		    alertMessage: function(msg){
		        var icon = '<i class="icon fa fa-warning" style="margin-right: 10px;"></i>';
		        $('.modal-title').empty();
		        $('.modal-body').empty();
		        $('.modal-title').append(icon+'Warning');
		        $('.modal-body').append(msg);
		        $('#basicModal').modal('show');
		    },

		    /* Configure message modal window for error */
		    errorMessage: function(msg){
		        var icon = '<i class="icon fa fa-ban" style="margin-right: 10px;"></i>';
		        $('.modal-title').empty();
		        $('.modal-body').empty();
		        $('.modal-title').append(icon+'Error');
		        $('.modal-body').append(msg);
		        $('#basicModal').modal('show');
		    }

		};
	};
	return Helper;
});