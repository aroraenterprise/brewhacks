'use strict';

describe('Service: BackendService', function () {

  // load the service's module
  beforeEach(module('frontendApp'));

  // instantiate service
  var BackendService;
  beforeEach(inject(function (_BackendService_) {
    BackendService = _BackendService_;
  }));

  it('should do something', function () {
    expect(!!BackendService).toBe(true);
  });

});
