function initData(metadata) {
	console.log(metadata);
	window.metadata = metadata;
}

var app = angular.module('app', ["ngRoute"]);

app.controller('ctrl', function($scope, $location, $http, $rootScope, $filter, $window) {
  $scope.data = {};
  $scope.data.modelData = {};
  $scope.data.modelData.augmentations = {"bin_uniform":false, "simple_uniform":false, "skew":false};

$scope.doit = function() {
   console.log($scope.sortBy);
}

$scope.initMetadata = function() {
//	console.log($window.metadata)
	$scope.data.training_data = $window.metadata;
	console.log($scope.data.training_data);
}


$scope.train = function() {
	$scope.data.modelData.datasets = [];
	for (i = 0; i < $scope.data.training_data.length; i++) {
		$scope.data.modelData.datasets.push( {"date":$scope.data.training_data[i].date,
					"use": $scope.data.training_data[i].use } );
	}

	console.log($scope.data.modelData);

	$.ajax({
		url: '/train',
		contentType: "application/json",
		type: 'POST',
		data: JSON.stringify({"modelData":$scope.data.modelData})
	})
	.done(function(result) {
		console.log(result);
		$window.location.reload();
	 })
}




$scope.selectDatasetForDelete = function( dataset ) {
		$scope.deleteThisDataset = dataset;
}

$scope.deleteDataset = function() {
        console.log($scope.deleteThisDataset);
	$.ajax({
		url: '/delete',
		contentType: "application/json",
		type: 'POST',
		data: JSON.stringify({"dataset":$scope.deleteThisDataset.date})
	})
	.done(function(result) {
		console.log(result);
		$window.location.reload();
	})
}

});
