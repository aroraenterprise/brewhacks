'use strict';

/**
 * @ngdoc service
 * @name frontendApp.DeliveryService
 * @description
 * # DeliveryService
 * Service to interface with delivery.com
 */
angular.module('frontendApp')
  .service('DeliveryService', function ($http, $log) {
    var service = this;
    this.beers = {};
    this.merchants = {};
    this.selectedMerchant = {'active': null};

    this.initialize = function(){
      return $http({
        url: '../assets/merchants.js',
        method: 'get',
        dataType: 'json'
      }).then(function(response){
        $log.debug(response.data);
        //angular.forEach(response.data, function(item){
        //
        //  service.merchants.push(merchant);
        //});
        //if (service.merchants.length > 0)
        //  service.selectedMerchant = {'active': service.merchants[0]}; // sets the first merchant as default active
      }, function(error){
        $log.debug(error);
      })
    }
  });
