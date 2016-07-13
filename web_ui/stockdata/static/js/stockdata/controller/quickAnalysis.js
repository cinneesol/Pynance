/**
 * controller for querying stocks
 * historical analysis and option chain analysis
 */

var quickAnalysisController = function($scope,quickAnalysisService){
	$scope.symbol="";
	$scope.quickAnalysisData = {};
	
	var processQuickAnalysisResponse = function(response){
		$scope.quickAnalysisData = response;
		console.log(JSON.stringify(response,null,4))
	}
	
	$scope.doQuickAnalysis = function(){
		$scope.quickAnalysisData = {};
		quickAnalysisService.quickAnalysis($scope.symbol).then(processQuickAnalysisResponse);
		
	}
	
}
angular.module("stockdata").controller('quickAnalysisController',['$scope','quickAnalysisService',quickAnalysisController]);