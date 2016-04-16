'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('MainCtrl', function ($log, $rootScope, DeliveryService, $scope) {
    $scope.merchants = DeliveryService.merchants;
    $scope.selectedMerchant = DeliveryService.selectedMerchant;
  });
