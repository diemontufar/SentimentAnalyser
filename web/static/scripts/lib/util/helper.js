/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       
 * ======================================================================== */

var statesList = {};
	statesList['VIC'] = 'Melbourne';
	statesList['NSW'] = 'Sydney';
	statesList['TAS'] = 'Hobart';
	statesList['QLD'] = 'Brisbane';
	statesList['NT'] = 'Darwin';
	statesList['WA'] = 'Perth';
	statesList['SA'] = 'Adelaide';

define(["moment"], function(Moment)
{
	"use strict";

	var Helper = function()
	{
		return {

			sentiment_icon : {positive:"fa-thumbs-o-up",negative:"fa-thumbs-o-down",neutral:"fa-meh-o"},

			date_options : {
					drops:'up',
                    startDate: moment().subtract(29, 'days'),
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
                    // buttonClasses: ['btn btn-default'],
                    // applyClass: 'btn-sm btn-primary',
                    // cancelClass: 'btn-sm',
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
	                                                'total' : country.population.total,
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
			              chart: {
			                  type: 'column'
			              },
			              credits: {
						      enabled: false
						  },
						  exporting: {
						  	enabled: true
						  },
			              title: {
			                  text: title
			              },
			              xAxis: {
			                  categories: labelsStates
			              },
			              yAxis: {
			                  title: {
			                      text: yAxisLabel
			                  }
			              },
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
			              series: [{
			                  name: 'Positive',
			                  data: positives,
			                  color: '#00aff0'
			              }, 
			              {
			                  name: 'Negative',
			                  data: negatives,
			                  color: '#f05032'
			              },
			              {
			                  name: 'Neutral',
			                  data: neutrals,
			                  color: '#54b847'
			              }]
		          	};

			      }else{
			      	return undefined;
			      }

			      return dataChart;


            },

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

	            	  		var dataT ={
						                name: type + hashtag,
						                data: [[countTop,count]]
						               };

							dataP.push(dataT);
							
						});

            	  		if (dataP ===undefined || dataP ===null || dataP.length == 0){

            	  			// labelsStates.push(null);

            	  		}else{
            	  			for (var i=0;i<5;i++){
            	  				seriesP.push(dataP[i]);
            	  			} 
            	  			labelsStates.push(statesList[key]);
            	  			countTop++;
            	  		}

            	  		

            	  	});

            	  	console.log(labelsStates);

	            	  var dataChart = {
							        chart: {
							            type: 'column'
							        },
							        credits: {
									      enabled: false
									  },
							        title: {
							            text: title
							        },
							        exporting: {
									  	enabled: true
									  },
							        xAxis: {
							        	categories: labelsStates
							        },
							        
							        yAxis: {
							            min: 0,
							            title: {
							                text: yAxisLabel
							            },
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
							        "series": seriesP
							};

			      }else{
			      	return undefined;
			      }

			      return dataChart;


            },

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
							        chart: {
							            type: 'line'
							        },
							        title: {
							            text: title
							        },
							        subtitle: {
							            text: 'Looking at the most Happiest and Misserable suburb in: ' + city
							        },
							        credits: {
									      enabled: false
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

            getPopulationVsTweetsBarChartData: function(data,title,yAxisLabel){

            	if (data !== undefined && data !== null){

            	  	var cultures = [];
            	  	var population = [];
            	  	var tweets = [];

            	  	$.each(data,function(key,value){

            	  		cultures.push(value.countryOfBirth);
        	  			population.push(value.total);
            	  		tweets.push(value.tweets);

            	  	});

		            var dataChart =	{
			              chart: {
			                  zoomType: 'xy'
			              },
			              credits: {
						      enabled: false
						  },
						  exporting: {
						  	enabled: true
						  },
			              title: {
			                  text: title
			              },
			              xAxis: {
			                  categories: cultures
			              },
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

		       
		        $("#section-cultures").fadeIn(2000);
		        $("#section-map").fadeIn(2000);
		        
		        $('#section-piechart-cultures').fadeOut(2000);
		        $('#section-linechart-sentiment').fadeOut(2000);
		        $('#section-linechart-cultures').fadeOut(2000);

		        $('#disclaimer-sentiment').fadeOut(2000);
		        $("#section-feed").fadeOut(2000);
		        $("#section-toptwitterers").fadeOut(2000);
		        $("#section-toptrends").fadeOut(2000);
		        $("#section-topcountries").fadeOut(2000);
		        $("#section-overallsentiment").fadeOut(2000);
		        $("#div-totals").fadeOut(2000);
		        // $('#section-bar-chart').css('visibility','hidden');
		        $('#section-chart').fadeOut(2000);


		    },

		  	isInStateList: function(state){

				return statesList[state] != undefined;

		  	},

		  	getCityName: function(id){
			  
			  return statesList[id];

			},

			infoMessage: function(msg){
		        var icon = '<i class="icon fa fa-info" style="margin-right: 10px;"></i>';
		        $('.modal-title').empty();
		        $('.modal-body').empty();
		        $('.modal-title').append(icon+'Info');
		        $('.modal-body').append(msg);
		        $('#basicModal').modal('show');
		    },

		    alertMessage: function(msg){
		        var icon = '<i class="icon fa fa-warning" style="margin-right: 10px;"></i>';
		        $('.modal-title').empty();
		        $('.modal-body').empty();
		        $('.modal-title').append(icon+'Warning');
		        $('.modal-body').append(msg);
		        $('#basicModal').modal('show');
		    },

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