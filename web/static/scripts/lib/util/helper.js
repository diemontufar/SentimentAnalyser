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
                    dateLimit: { days: 90 },
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