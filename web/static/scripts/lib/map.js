define([], function()
{
  "use strict";

  var Map = function()
  {
    return {

    map : this.map,


    /* Initialize Google maps PageModule */
    setCenter: function(lat,long) {
       map.setCenter(new google.maps.LatLng(lat,long));
    },

    getMap: function(){
        return this.map;
    }

    };
  };

  return Map;

});

