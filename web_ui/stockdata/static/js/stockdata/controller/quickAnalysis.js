/**
 * controller for querying stocks
 * historical analysis and option chain analysis
 */

var quickAnalysisController = function($scope,quickAnalysisService){
	$scope.symbol="";
	$scope.qaData = {"symbol":"MT"};
	
	var processQuickAnalysisResponse = function(response){
		$scope.qaData = response;
		console.log(JSON.stringify($scope.qaData,null,4))
	}
	
	$scope.doQuickAnalysis = function(){
		$scope.qaData = {};
		quickAnalysisService.quickAnalysis($scope.symbol).then(processQuickAnalysisResponse);
		
	}
	
}
angular.module("stockdata").controller('quickAnalysisController',['$scope','quickAnalysisService',quickAnalysisController]);