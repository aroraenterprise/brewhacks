'use strict';

/**
 * @ngdoc overview
 * @name frontendApp
 * @description
 * # frontendApp
 *
 * Main module of the application.
 */
angular
  .module('frontendApp', [
    'ngAnimate',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngSanitize',
    'ngTouch',
    'ui.router',
    'chart.js',
    'ui.bootstrap',
    'angularMoment',
    'ngMap',
    'angular-nicescroll'
  ])
  .config(function ($urlRouterProvider, $stateProvider) {
    $urlRouterProvider.otherwise('/home');

    $stateProvider

    // HOME STATES AND NESTED VIEWS ========================================
      .state('home', {
        abstract: true,
        url: '/home',
        controller: 'MainCtrl',
        template: '<div class="container-fluid mimin-wrapper">' +
        '<div ui-view="left-menu"></div>' +
        '<div ui-view="content"></div>' +
        '</div>',
        resolve: {
          '': function (BackendService) {
            return BackendService.initialize()
          }
        }
      })
      .state('home.welcome', {
        url: '',
        views: {
          'left-menu': {
            templateUrl: '../views/left-menu.html',
            controller: 'SidebarCtrl'
          },
          'content': {
            templateUrl: '../views/main.html',
            controller: 'WelcomeCtrl'
          }
        }
      });
  });
