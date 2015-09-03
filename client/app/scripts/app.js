/*
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
Code distributed by Google as part of the polymer project is also
subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt
*/

(function(document) {
  'use strict';

  // Grab a reference to our auto-binding template
  // and give it some initial binding values
  // Learn more about auto-binding templates at http://goo.gl/Dx1u2g
  var app = document.querySelector('#app');

  // Listen for template bound event to know when bindings
  // have resolved and content has been stamped to the page
  app.addEventListener('dom-change', function() {
    // console.log('Our app is ready to rock!');
  });

  // See https://github.com/Polymer/polymer/issues/1381
  window.addEventListener('WebComponentsReady', function() {
    // imports are loaded and elements have been registered
  });

  // Main area's paper-scroll-header-panel custom condensing transformation of
  // the appName in the middle-container and the bottom title in the bottom-container.
  // The appName is moved to top and shrunk on condensing. The bottom sub title
  // is shrunk to nothing on condensing.
  addEventListener('paper-header-transform', function(e) {
    var appName = document.querySelector('#mainToolbar .app-name');
    var middleContainer = document.querySelector('#mainToolbar .middle-container');
    var bottomContainer = document.querySelector('#mainToolbar .bottom-container');
    var detail = e.detail;
    var heightDiff = detail.height - detail.condensedHeight;
    var yRatio = Math.min(1, detail.y / heightDiff);
    var maxMiddleScale = 0.50;  // appName max size when condensed. The smaller the number the smaller the condensed size.
    var scaleMiddle = Math.max(maxMiddleScale, (heightDiff - detail.y) / (heightDiff / (1-maxMiddleScale))  + maxMiddleScale);
    var scaleBottom = 1 - yRatio;

    // Move/translate middleContainer
    Polymer.Base.transform('translate3d(0,' + yRatio * 100 + '%,0)', middleContainer);

    // Scale bottomContainer and bottom sub title to nothing and back
    Polymer.Base.transform('scale(' + scaleBottom + ') translateZ(0)', bottomContainer);

    // Scale middleContainer appName
    Polymer.Base.transform('scale(' + scaleMiddle + ') translateZ(0)', appName);
  });

  app.hideDrawer = function() {
    var drawerPanel = document.querySelector('#paperDrawerPanel');
    if (drawerPanel.narrow) {
      drawerPanel.closeDrawer();
    }
  };

  // Close drawer after menu item is selected if drawerPanel is narrow
  app.onDataRouteClick = function() {
    app.hideDrawer();
    app._selectedRoute();
    // console.log('on data route clicked, sending page view');
    // ga('send', 'pageview', page.current);
  };

  app.changePage = function(url) {
    app.hideDrawer();
    page(url, null, null, false);
    console.log('we are doing a page change');
    app._selectedRoute();
  };

  app.onHistoryRouteClick = function() {
    app.onDataRouteClick();
    // If we don't have a date range, lets get a date range.
    if (!app.startDate || !app.endDate) {
      app.$.rangeSelector.open();
    }
  };

  app.selectedRoute = 'map';
  app._selectedRoute = function() {
    app.showingPost = false;
    app.showingMap = false;
    app.showingCurrent = false;
    app.showingHistory = false;
    app.showingBlog = false;

    if (app.route === 'now' || app.route === 'history') {
      app.selectedRoute = 'map';
      app.showingMap = true;
      if (app.route === 'current') {
        app.showingCurrent = true;
      } else if (app.route === 'history') {
        app.showingHistory = true;
      }
    } else {
      app.selectedRoute = app.route;
      if (app.route === 'post') {
        app.showingPost = true;
      } else if (app.route === 'blog') {
        app.showingBlog = true;
      }
    }
  };

  app.currentLocation = 'Somewhere in the world';
  app.locationSince = 'Since whenever';

  app.handleCurrent = function() {
    var c = app.current;
    var loc;
    if (c.city) {
      loc = c.city + ', ';
    } else if (c.state) {
      loc = c.state + ', ';
    } else {
      loc = 'Somewhere in ';
    }
    if (c.country) {
      loc = loc + c.country;
    }
    if (loc === 'Somewhere in ') {
      loc = 'No idea where he is...';
    }
    app.currentLocation = loc;

    // I would like to create neater status info server side.
    // TODO(#7)
    /*jshint unused:true */
    app.locationSince = 'There for ' + c.elapsed_humanized;
  };

  app.historyUrl = '';
  app.showingHistory = false;

  app.makeHistoryUrl = function() {
    if (app.startDate) {
      app.historyUrl = ('/history/' + encodeURIComponent(app.startDate) +
                        '/to/' + encodeURIComponent(app.endDate));
    } else {
      app.historyUrl = '/history';
    }
  };
  app.makeHistoryUrl();

  addEventListener('blog-post-selected', function(event) {
    app.postId = event.detail.postId;
    if (event.detail.link) {
      var arr = event.detail.link.split('/');
      var title = arr[arr.length - 2];
      app.changePage('/blog/' + app.postId + '/' + title);
    } else {
      app.changePage('/blog/' + app.postId);
    }
  });

  addEventListener('date-range-updated', function() {
    app.makeHistoryUrl();
    app.changePage(app.historyUrl);
  });

  app.showRangeSelector = function() {
    app.$.rangeSelector.open();
  };

  app.returnToHistory = function() {
    app.changePage(app.historyUrl);
  };

})(document);
