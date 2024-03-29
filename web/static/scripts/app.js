/* ========================================================================
 * Author:            Diego Montufar
 * Date:              25 Feb 2015
 * Description:       Here we are defining all library dependecies and imports by using Requirejs.
 *                    Requirejs help us to structure a javascript project without having to explicitly
 *                    define <script> html tags on the index.html file. Also helps to import omptimized JS libraries
 *                    
 * ======================================================================== */

/*
* For any third party dependencies, like jQuery, place them in the lib folder.

* Configure loading modules from the lib directory,
* except for 'app' ones, which are in a sibling directory

*Versions:
* jQuery v2.0.2
* jQuery UI v1.10.3 
* Bootstrap v3.0.3
* SlimScroll v1.3.0
* date.format v1.1
*/

requirejs.config({
    "baseUrl": 'static/scripts/lib',
    "paths": {
        "app": "../app",
        "jquery": "jquery/jquery.min",
        "jquery.jqueryui": "jqueryui/jquery-ui-1.10.3.min",
        "jquery.bootstrap": "bootstrap/bootstrap.min",
        "slimscroll": "slimscroll/jquery.slimscroll.min",
        "dateformat": "util/date.format",
        "modules": "modules",
        "goog" : "util/goog",
        "propertyParser" : "util/propertyParser",
        "async" : "util/async",
        "helper": "util/helper",
        "dynatable": "dynatable/jquery.dynatable",
        "daterangepicker": "daterangepicker/daterangepicker",
        "moment": "daterangepicker/moment",
        "highcharts":"highcharts/highcharts",
        "exporting":"highcharts/modules/exporting",
        "nodatatodisplay":"highcharts/modules/no-data-to-display",
        "highcharts3d": "highcharts/highcharts-3d",
        "foamtree": "carrotsearch/carrotsearch.foamtree"
    },
    shim: {
        "jquery.bootstrap": {
            deps: ["jquery"]
        },
        "jquery.jqueryui": {
            deps: ["jquery"]
        },
        "slimscroll": {
            deps: ["jquery"]
        },
        "dynatable": {
            deps: ["jquery"]
        },
        "daterangepicker": {
            deps: ["jquery"]
        },
        "daterangepicker": {
            deps: ["jquery.bootstrap"]
        },
        "highcharts": {
            deps: ["jquery"]
        },
        "exporting": {
            deps: ["highcharts"]
        },
        "nodatatodisplay":{
            deps: ["highcharts"]
        },
        "highcharts3d":{
            deps: ["highcharts"]
        },
        "foamtree": {
            deps: ["jquery"]
        }

    }
});

// Start loading the main app file. Put all of
// your application logic in there.
requirejs(['app/main']);

