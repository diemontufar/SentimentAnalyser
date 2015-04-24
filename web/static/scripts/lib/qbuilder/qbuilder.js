/* ========================================================================
 * Author:            Diego Montufar
 * Date:              05 Mar 2015
 * Description:       The Query Builder is responsible of creating and building queries using the ESQ library 
 * ======================================================================== */

define(['esq/esq'], function(ESQ) {

	/* Constructor */
    var QBuilder = function() {
    };


    /** Method: buildBasicMatchSearch
    *	Description: Allows you to search for a value using the match option
    *	Parameters:
    *		type: query/bool
    *		key: key field you are searching for
    *		value: the vaule you are searching for  
    **/
    QBuilder.prototype.buildBasicMatchSearch = function(type,key,value){
    	
    	var esq = new ESQ();
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
    	
    	var esq = new ESQ();
    	esq.query(type,['must'],{ match: { key : value } });

    	return JSON.stringify(esq.getQuery(), null, 2);
    };

    /** Method: buildSearchByTerm
    *   Description: Perform basic search by term
    *   Parameters:
    *       term: the term you are searching for  
    **/
    QBuilder.prototype.buildSearchByTerm = function(term){
        
        var esq = new ESQ();
        esq.query('query',{'filtered':{'query': {'match': {'text': {'query': term,'operator': 'or'}}},'filter': {'term': {'lang': 'en'}}}});

        return JSON.stringify(esq.getQuery(), null, 2);
    };

    /** Method: buildPaginatedSearchByTerm
    *   Description: Perform basic search by term with pagination
    *   Parameters:
    *       term: the term you are searching for  
    *       start: the start of the paginated search
    *       size: size of the pagination
    **/
    QBuilder.prototype.buildPaginatedSearchByTerm = function(term, start , size){

        var esq = new ESQ();
        esq.query('query',{'filtered':{'query': {'match': {'text': {'query': term,'operator': 'or'}}},'filter': {'term': {'lang': 'en'}}}});
        esq.query('from',start);
        esq.query('size',size);

        return JSON.stringify(esq.getQuery(), null, 2);
    };

    QBuilder.prototype.buildBasicAggregation = function(term,field,size){

        var query = {"size": 0, "query": {"query_string": {"analyze_wildcard": true, "query": "*"} }, "aggs": {"2": {"terms": {"field": field, "size": size, "order": {"_count": "desc"} } } } };
        return JSON.stringify(query, null, 2);
    };

	return QBuilder;
});