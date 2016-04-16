'use strict';

describe('Controller: SidebarcontrollerCtrl', function () {

  // load the controller's module
  beforeEach(module('frontendApp'));

  var SidebarcontrollerCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SidebarcontrollerCtrl = $controller('SidebarcontrollerCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(SidebarcontrollerCtrl.awesomeThings.length).toBe(3);
  });
});
