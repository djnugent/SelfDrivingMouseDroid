function initData(metadata) {
//	console.log(metadata);
	window.metadata = metadata;
}

var app = angular.module('app', ["ngRoute"]);

app.controller('ctrl', function($scope, $location, $http, $rootScope, $filter, $window) {
  $scope.data = {};
  $scope.data.trainingDatasets = [];
  $scope.data.testingDatasets = [];

 $scope.test = function() {
   console.log("test");
 }

 $scope.initMetadata = function() {
//	console.log($window.metadata)
	$scope.data.training_data = JSON.parse($window.metadata);
	console.log($scope.data.training_data);
	console.log($scope.data.training_data[0]);
}

 $scope.addTrain = function(date) {
	var index = $scope.data.testingDatasets.indexOf(date);
	if (index > -1)	$scope.data.testingDatasets.splice (index, 1);
	$scope.data.trainingDatasets.push(date);
	console.log($scope.data);
}

 $scope.addTest = function(date) {
	var index = $scope.data.trainingDatasets.indexOf(date);
	if (index > -1) $scope.data.trainingDatasets.splice(index, 1);
	$scope.data.testingDatasets.push(date);
	console.log($scope.data);
}

 $scope.train = function() {
	console.log($scope.data);
	$.ajax({
		url: '/train',
		contentType: "application/json",
		type: 'POST',
		data: JSON.stringify({"trainingDatasets":$scope.data.trainingDatasets,
				      "testingDatasets":$scope.data.testingDatasets})
	})
	.done(function(result) {
		console.log(result);
	 })
}

 $scope.refetch = function() {
	console.log("JavaScript refetching");
	$.ajax({
		url: '/refetch',
		contentType: "applicaiton/json",
		type: 'POST',
		data: "",
	})
	.done(function(result) {
		console.log(result);
	})
}

 $scope.initGraph = function() {
var results = {};
results.loss = [10, 10, 15, 16, 20, 25, 40, 55, 70, 78, 87, 92, 99, 100];
var ctxLineGraph = $("#lineGraph").get(0).getContext("2d");

// if (lineGraph != null) {
// 	console.log("destroying chart!");
// 	lineGraph.destroy();
// }

lineGraph = new Chart(ctxLineGraph, {
		type: 'line',
		data: {
				labels:results.loss ,
				datasets: [/*{ HERE if you want multiple data sets on same graph
						label: 'Speed',
						data: ride.speed,
						backgroundColor: '#54997E',
						borderWidth: 1
				},*/
				{
					label: 'Loss',
					data: results.loss,
					backgroundColor: '#ffe2b5',
					borderWidth: 1
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
				scales: {
						yAxes: [{
								ticks: {
										beginAtZero:true
								}
						}]
				}
		}

});
}


/*

$scope.fetchData = function() {
  $scope.data.training_data = [];

  // Check for the various File API support.
  if (window.File && window.FileReader && window.FileList && window.Blob) {
  } else {
    alert('The File APIs are not fully supported in this browser.');
  }

  var fileInput = document.getElementById('file_input');
  console.log("File Input");
  console.log(fileInput);
  console.log(" ");

  for( i = 0; i < fileInput.files.length; i++) {
      if (fileInput.files[i].name == "metadata.txt") {
      //console.log("reading: " + fileInput.files[i].name);

      var reader = new FileReader();
        reader.onload = function(e){
          //console.log(e);
          var string = e.target.result;
          //console.log(string);

          var data = [];
          var cursor1 = 0;
          var cursor2 = 0;
          cursor1 = string.search(" Recorded By: ") + 15;
          cursor2 = string.indexOf("~", cursor1);
          data['recordedBy'] = string.substring( cursor1 , cursor2);

          cursor1 = string.search(" Location: ") + 11;
          cursor2 = string.indexOf("~", cursor1);
          data['location'] = string.substring( cursor1 , cursor2);

          cursor1 = string.search(" Batch Size: ") + 13;
          cursor2 = string.indexOf("~", cursor1);
          data['batchSize'] = string.substring( cursor1 , cursor2);

          cursor1 = string.search(" Obstacles: ") + 12;
          cursor2 = string.indexOf("~", cursor1);
          data['obstacles'] = string.substring( cursor1 , cursor2);

          cursor1 = string.search(" Pedestrians: ") + 14;
          cursor2 = string.indexOf("~", cursor1);
          data['pedestrians'] = string.substring( cursor1 , cursor2);

          cursor1 = string.search(" Tags: ") + 6
          cursor2 = string.indexOf("~", cursor1);
          data['tags'] = string.substring( cursor1 , cursor2);
          //startTag = cursor1 + 1;
          // data['tags'] = [];
          // while (startTag < cursor2 - 1) {
          //   endTag = string.indexOf(",", startTag);
          //   console.log(endTag);
          //   if (endTag == -1) { endTag = string.indexOf("~", startTag); console.log("new end " + endTag); }
          //   data['tags'].push( string.substring(startTag, endTag));
          //   startTag = endTag + 2;
          //   if (startTag == 0) break;
          // }

          cursor1 = string.search(" Notes: ") + 8;
          cursor2 = string.indexOf("~", cursor1);
          data['notes'] = string.substring( cursor1 , cursor2);

          cursor1 = string.search(" Date: ") + 7;
          cursor2 = string.indexOf("~", cursor1);
          data['date'] = string.substring( cursor1 , cursor2);

          console.log(data);

          $scope.data.training_data.push(data);
          $("#table").show();
          console.log($scope.data);
          $scope.$apply();
        };
         reader.readAsText(fileInput.files[i]);
    }
  }



}

$scope.run = function() {
  console.log("running");

}*/

});
