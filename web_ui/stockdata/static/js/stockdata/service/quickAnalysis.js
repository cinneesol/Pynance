var quickAnalysisService = function($http){
	
	var processResponse = function(response){
		return response.data;
	}
	
	var quickAnalysis = function(symbol){
		return $http.post("/stockdata/rest/quick_analysis.ws",{
			symbol:symbol
		}).then(processResponse);
	}
	
	return{
		quickAnalysis:quickAnalysis
	}
}										

angular.module('stockdata').factory('quickAnalysisService',["$http",quickAnalysisService]);