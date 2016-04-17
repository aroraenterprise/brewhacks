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
        if (response.data)
          $scope.selectedBeer['transactions'] = response.data.list;
      })
    };
    $scope.$watch($scope.merchant, function(){
      $scope.selectBeer($scope.merchant.active.products[0]);
    });

  });
