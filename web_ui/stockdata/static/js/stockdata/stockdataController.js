(function(){
	var stockdataController = function($scope){
		console.log("Hello angularjs");
	};
	angular.module('stockdata').controller('stockdataController',['$scope',stockdataController])
})()