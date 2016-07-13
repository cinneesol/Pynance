var findNearEntryPointService = function($http){
	
	var processResponse = function(response){
		return response.data;
	}
	
	var findNearTargetEntry = function(percentage,profit){
		return $http.post("/stockdata/rest/near_target_entry_point.ws",{
			profit:profit,
			percent:percentage
		}).then(processResponse);
	}
	
	return{
		findNearTargetEntry:findNearTargetEntry
	}
}										

angular.module('stockdata').factory('findNearEntryPointService',["$http",findNearEntryPointService]);