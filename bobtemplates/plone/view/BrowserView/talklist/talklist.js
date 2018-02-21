'use strict';

//
// module depends on mobile-angular-ui
//
var app = angular.module('TalkListApp', [
  'mobile-angular-ui',
]);


app.controller('MainController', function($rootScope, $scope, $http) {

  $scope.items = [];
  $scope.login = function(login, passwd) {
    $http.post('/Plone/@login',
              {'login':login,
               'password':passwd},
              {headers:
               {'Content-type':'application/json',
                'Accept':'application/json'}}).
      success(function(data, status, headers, config){
        localStorage.setItem('jwtoken', data.token);
      }).
      error(function(data, status, headers, config){
        alert('Could not log you in');
      });
  };

  $scope.is_logged_in = function() {
    // we assume the user is logged in when he has a JWT token (that is naive)
    return localStorage.getItem('jwtoken') != null;
  };

  $scope.submit_talk = function(subject, summary) {
    $http.post('/Plone/talks',
               {'@type':'talk',
                'type_of_talk':'Lightning Talk',
                'audience':['Beginner','Advanced','Professionals'],
                'title':subject,
                'description':summary},
               {headers:
                {'Content-type':'application/json',
                 'Authorization': 'Bearer ' + localStorage.getItem('jwtoken'),
                 'Accept':'application/json'}}).
      success(function(data, status, headers, config){
        if(status==201) { // created
          $scope.load_talks();
        }
      }).
      error(function(data, status, headers, config){
        // according to docs, status can be 400 or 500
        // we check wether the token has expired - in this case,
        // we remove it from localStorage and disply the login page.
        // In all other cases, we display the message received
        // from Plone
        if ( (status == 400) && (data.type == 'ExpiredSignatureError') ) {
          localStorage.removeItem('jwtoken');
          location.reload();
        } else {
          // reason/error msg is contained in response body
          alert(data.message);
        }
      });
  };

  $scope.load_talks = function() {
    $http.get('/Plone/talks',
              {headers:{'Accept':'application/json'}}).
      success(function(data, status, headers, config) {
        $scope.items = [];
        // get the paths of the talks
        var paths = [];
        for (var i=0; i < data.items_total; i++) {
          paths.push(data.items[i]['@id'])
        }
        // next get details for each talk
        for (var i=0; i < paths.length; i++) {
          $http.get(paths[i],
                    {headers:{'Accept':'application/json'}}).
            success(function(talkdata, status, headers, config) {
              // this is an angular 'promise' - we cannot
              // rely on variables from an outer scope
              var path = talkdata['@id'];
              var talk = {
                'pos': paths.indexOf(path),
                'path': path,
                'title': talkdata.title,
                'type': talkdata.type_of_talk,
                'speaker': (talkdata.speaker != null) ? talkdata.speaker : talkdata.creators[0],
                'start': talkdata.start,
                'subjects': talkdata.subjects,
                'details': (talkdata.details != null) ? talkdata.details.data : talkdata.description
              }
              $scope.items.push(talk);

            }).
            error(function(talkdata, status, headers, config) {});
        }
      }).
    error(function(data, status, headers, config) {
      $scope.items = [];
    });
  };

  // initialize
  $scope.load_talks();
});
