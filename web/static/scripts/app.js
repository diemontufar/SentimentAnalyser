// For any third party dependencies, like jQuery, place them in the lib folder.

// Configure loading modules from the lib directory,
// except for 'app' ones, which are in a sibling
// directory.

//Versions:
//jQuery v2.0.2
//jQuery UI v1.10.3 
//Bootstrap v3.0.3
//SlimScroll v1.3.0
//date.format v1.1

requirejs.config({
    "baseUrl": 'static/scripts/lib',
    "paths": {
        "app": "../app",
        "jquery": "jquery/jquery.min",
        "jquery.jqueryui": "jqueryui/jquery-ui-1.10.3.min",
        "jquery.bootstrap": "bootstrap/bootstrap.min",
        "slimscroll": "slimscroll/jquery.slimscroll.min",
        "dateformat": "date.format",
        "modules": "modules",
        "goog" : "goog",
        "propertyParser" : "propertyParser",
        "helper": "helper",
        "map": "map",
        "chart": "chart"
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
        }
    }
});

// Start loading the main app file. Put all of
// your application logic in there.
requirejs(['app/app-sentiment']);

