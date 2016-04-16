'use strict';

describe('Controller: WelcomecontrollerCtrl', function () {

  // load the controller's module
  beforeEach(module('frontendApp'));

  var WelcomecontrollerCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    WelcomecontrollerCtrl = $controller('WelcomecontrollerCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(WelcomecontrollerCtrl.awesomeThings.length).toBe(3);
  });
});
