'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:SidebarCtrl
 * @description
 * # SidebarCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('SidebarCtrl', function ($scope, $log, $timeout, DeliveryService) {
    $scope.selectMerchant = function(item){
      DeliveryService.selectedMerchant.active = item;
    };

    $scope.clock = 0;
    $scope.tickInterval = 1000; //ms

    var tick = function() {
        $scope.clock = Date.now(); // get the current time
        $timeout(tick, $scope.tickInterval); // reset the timer
    };

    // Start the timer
    $timeout(tick, $scope.tickInterval);
  });
