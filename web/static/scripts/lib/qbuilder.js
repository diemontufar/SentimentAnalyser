/* ========================================================================
 * Author:            Diego Montufar
 * Date:              05 Mar 2015
 * Description:       The Query Builder is responsible of creating and building queries using the ESQ library 
 * ======================================================================== */

define(['esq'], function(ESQ) {

    var esq_obj = null;

	/* Constructor */
    var QBuilder = function() {
    	this.esq_obj = new ESQ();
    };


    /** Method: buildBasicMatchSearch
    *	Description: Allows you to search for a value using the match option
    *	Parameters:
    *		type: query/bool
    *		key: key field you are searching for
    *		value: the vaule you are searching for  
    **/
    QBuilder.prototype.buildBasicMatchSearch = function(type,key,value){
    	
    	var esq = this.esq_obj;
    	esq.query(type, { match: { key : value } });

    	return JSON.stringify(esq.getQuery(), null, 2);
    };

    /** Method: buildBasicMatchSearch
    *	Description: Allows you to search for a value using the match option
    *	Parameters:
    *		type: query/bool
    *		key: key field you are searching for
    *		value: the vaule you are searching for  
    **/
    QBuilder.prototype.buildMustMatchSearch = function(type,key,value){
    	
    	var esq = this.esq_obj;
    	esq.query(type,['must'],{ match: { key : value } });

    	return JSON.stringify(esq.getQuery(), null, 2);
    };

    /** Method: buildBasicFilteredSearch
    *   Description: TODO: Change this to be more generic!!!!
    *   Parameters:
    *       term: the term you are searching for  
    **/
    QBuilder.prototype.buildBasicFilteredSearch = function(term){
        
        var esq = this.esq_obj;
        esq.query("query", {"filtered":{"query":{"match":{"text":{"query":term,"operator":"or"}}},"strategy":"query_first"}});

        return JSON.stringify(esq.getQuery(), null, 2);
    };

	return QBuilder;
});