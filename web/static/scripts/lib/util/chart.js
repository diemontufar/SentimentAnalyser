define([], function()
{
  "use strict";

  var Chart = function()
  {
    return {

    chart : new google.visualization.PieChart(document.getElementById('piechart_3d')),

    initializeChart: function(){
        google.maps.event.addDomListener(window, 'load', this.chartInitializer);
    },

    /* Initialize Google maps PageModule */
    chartInitializer: function() {
        //return new google.visualization.PieChart(document.getElementById('piechart_3d'));
    },

    getChart: function(){
        return this.chart;
    },

    /* Draw changes on Chart */
      drawPieChart:function(data){
        var options = {
          //title: 'My Daily Activities',
            pieHole: 0.4,
            is3D: true,
            colors: ['#00aff0', '#f05032', '#54b847']
          };

          if ( data!== null && this.chart!== null){
            this.chart.draw(data, options);
          }else{
            console.log("Error drawing pie chart");
          }
      }

    };
  };
  return Chart;
});