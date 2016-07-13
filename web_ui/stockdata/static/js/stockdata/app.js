var sd=angular.module('stockdata', ['ui.router']);

sd.config(function($stateProvider,$urlRouterProvider){
	$urlRouterProvider.otherwise('/');
	
	//set up states for the stockdata web application
	$stateProvider.state('/',{
		url:'/',
		templateUrl: '/stockdata/landing.html'
	})
	.state('/findnearentry',{
		url:'/findnearentry',
		templateUrl: '/stockdata/findnearentry.html',
		controller: 'findNearEntryPointController'
	})
});