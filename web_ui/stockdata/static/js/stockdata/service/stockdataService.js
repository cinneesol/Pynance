(function(){
	
	var stockdataService = function($http){
		
		var processNearTargetEntryResponse = function(response){
			
			return response;
		}
		
		var getNearTargetEntry = function(entry,profit){
			return $http.post('/stockdata/rest/near_target_entry_point.ws', {
				profit:profit,
				percent:entry
			});
		}
		
		return {
			getNearTargetEntry: getNearTargetEntry,
		}
	}
	
	angular.module('stockdata').factory('stockdataService',['$http', stockdataService]);
})()