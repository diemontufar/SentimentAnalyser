var statesList = {};
statesList['VIC'] = 'Melbourne';
statesList['NSW'] = 'Sydney';
statesList['TAS'] = 'Hobart';
statesList['QLD'] = 'Brisbane';
statesList['NT'] = 'Darwin';
statesList['WA'] = 'Perth';
statesList['SA'] = 'Adelaide';

var coordinatesList = {};
coordinatesList['VIC'] = [-37.816667,144.966667,11]; //lat,lang,zoom
coordinatesList['TAS'] = [-42.8819032,147.3238148,9]; //lat,lang,zoom

coordinatesList['NSW'] = [-33.8674869,151.2069902,11]; //lat,lang,zoom
coordinatesList['QLD'] = [-27.4710107,153.0234489,11]; //lat,lang,zoom
coordinatesList['WA'] = [-31.9535959,115.8570118,11]; //lat,lang,zoom
coordinatesList['NT'] = [-12.4628271,130.8417772,11]; //lat,lang,zoom
coordinatesList['SA'] = [-34.9286212,138.5999594,11]; //lat,lang,zoom

var innermelbourne = [
'206011105',
'206011106',
'206011107',
'206011108',
'206011109',
'206021110',
'206021111',
'206021112',
'206031113',
'206031114',
'206031115',
'206031116',
'206041117',
'206041118',
'206041119',
'206041120',
'206041121',
'206041122',
'206041123',
'206041124',
'206041125',
'206041126',
'206041127',
'206051128',
'206051129',
'206051130',
'206051131',
'206051132',
'206051133',
'206051134',
'206061135',
'206061136',
'206061137',
'206061138',
'206071139',
'206071140',
'206071141',
'206071142',
'206071143',
'206071144',
'206071145'];

var hobart = [
'601011001',
'601011002',
'601011003',
'601021004',
'601021005',
'601021006',
'601021007',
'601021008',
'601021009',
'601021010',
'601021011',
'601021012',
'601031013',
'601031014',
'601031015',
'601031016',
'601031017',
'601031018',
'601031019',
'601031020',
'601031021',
'601041022',
'601041023',
'601041024',
'601041025',
'601041026',
'601051027',
'601051028',
'601051029',
'601051030',
'601051031',
'601051032',
'601051033',
'601061034',
'601061035'
];

function getCityName(id){
  return statesList[id];
}

function isInStateList(value) {
  return statesList[value] != undefined;
}

function isInInnerMelbourne(value) {
  return innermelbourne.indexOf(value) > -1;
}

function isInHobart(value) {
  return hobart.indexOf(value) > -1;
}

function getLat(id){
	return coordinatesList[id][0];
}

function getLang(id){
	return coordinatesList[id][1];
}

function getZoom(id){
	return coordinatesList[id][2];
}