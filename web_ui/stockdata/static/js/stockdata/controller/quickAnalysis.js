/**
 * Quick analysis controller for querying stocks
 * near target entry and profit points
 */

var quickAnalysisController = function($scope,quickAnalysisService){
	$scope.candidates = []
	
	var logresponse = function(result){
		$scope.candidates=result
		console.log(JSON.stringif($scope.candidates,null,4))
	}
	
	quickAnalysisService.findNearTargetEntry(.01,.01).then(logresponse);
	
	
}
angular.module("stockdata").controller('quickAnalysisController',['$scope','quickAnalysisService',quickAnalysisController]);