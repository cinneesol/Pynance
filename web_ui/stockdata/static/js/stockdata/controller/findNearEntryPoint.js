/**
 * Quick analysis controller for querying stocks
 * near target entry and profit points
 */

var findNearEntryPointController = function($scope,findNearEntryPointService){
	$scope.candidates = []
	$scope.percentage=1;
	$scope.profit=1;
	var logresponse = function(result){
		$scope.candidates=result
	}
	
	$scope.getCandidates = function(){
		var percent = $scope.percentage/100;
		var profit = $scope.profit/100;
		findNearEntryPointService.findNearTargetEntry(percent,profit).then(logresponse);
	}
	
	$scope.getCandidates();
	
}
angular.module("stockdata").controller('findNearEntryPointController',['$scope','findNearEntryPointService',findNearEntryPointController]);