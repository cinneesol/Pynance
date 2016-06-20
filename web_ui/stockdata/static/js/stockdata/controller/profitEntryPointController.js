(function(){
	var stockdataController = function($scope, stockdataService){
		
		$scope.candidates = []
		$scope.profitPercent = 1;
		$scope.entryPricePercent = 1;
		
		$scope.searchNearTargetEntry = function(){
			stockdataService.
			getNearTargetEntry($scope.entryPricePercent/100 , $scope.profitPercent/100)
			.then(processResponse)
			
		}
		var processResponse = function(response){
			if(response.status == 200){
				$scope.candidates = response.data;
				console.log(JSON.stringify($scope.candidates,null,4))
			} else{
				alert("Error code from server: "+response.status)
			}
		}
		
		stockdataService.getNearTargetEntry($scope.entryPricePercent/100 , $scope.profitPercent/100).then(processResponse)
		
	};
	angular.module('stockdata').controller('profitEntryPointController',['$scope','stockdataService',stockdataController])
})()