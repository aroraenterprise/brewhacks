'use strict';

describe('Service: DeliveryService', function () {

  // load the service's module
  beforeEach(module('frontendApp'));

  // instantiate service
  var DeliveryService;
  beforeEach(inject(function (_DeliveryService_) {
    DeliveryService = _DeliveryService_;
  }));

  it('should do something', function () {
    expect(!!DeliveryService).toBe(true);
  });

});
