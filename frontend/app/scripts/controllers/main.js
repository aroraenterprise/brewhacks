'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('MainCtrl', function ($log, $rootScope, BackendService, $scope) {
    $scope.merchants = BackendService.merchants;
    $scope.selectedMerchant = BackendService.selectedMerchant;
  });
