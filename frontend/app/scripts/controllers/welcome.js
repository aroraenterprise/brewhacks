'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:WelcomeCtrl
 * @description
 * # WelcomeCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('WelcomeCtrl', function ($log, $scope, BackendService) {
    $scope.merchant = $scope.selectedMerchant;
    $scope.selectedBeer = {};
    $scope.selectBeer = function(beer){
      $scope.selectedBeer = beer;
      $log.debug("look for beer: " + beer.id);
      BackendService.listTransactions({product_id: beer.id}).then(function(response){
        if (response.data) {
          $scope.selectedBeer['transactions'] = response.data.list;
          resetData();
        }
      })
    };
    $scope.$watch($scope.merchant, function(){
      $scope.selectBeer($scope.merchant.active.products[0]);
    });

    $scope.labels = [];
    $scope.series = ['Consumption', 'Temperature'];
    $scope.data = [[],[]];

    function resetData(){
      $scope.labels = [];
      $scope.data = [[],[]];
      var myData = {};
      var lastTimestamp;
      angular.forEach($scope.selectedBeer.transactions, function(transaction, index){
        var time = (new Date(transaction.timestamp)).getTime();
        if (time in myData) {
          myData[time]['count'] += 1;
          myData[time]['trasaction'] = transaction;
        } else {
          myData[time] = {
            count: 1,
            transaction: transaction
          };
        }
      });
      $log.debug(myData);

      var counter = 0;
      var lastTemp = 0;
      angular.forEach(myData, function(datapoint, timestamp){
        $scope.data[0].push(datapoint.count * 3);
        if (counter % 2 == 0) {
          $scope.labels.push(timestamp);
          lastTemp = datapoint.transaction.farenheit / 5;
          $scope.data[1].push(lastTemp);
        }
        else {
          $scope.labels.push('');
          $scope.data[1].push(lastTemp)
        }
        counter++;
      });
    }
    //$scope.onClick = function (points, evt) {
    //  console.log(points, evt);
    //};

  });
