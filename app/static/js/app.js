var markers = [];
var map = null;

function ensureInitialized() {
  if (map == null) {
    initialize();
  }
}

function initialize() {
  var mapOptions = {
    zoom: 4
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  updateData();
}

// Sets the map on all markers in the array.
function setAllMap(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setAllMap(null);
}

// Shows any markers currently in the array.
function showMarkers() {
  setAllMap(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}

function updateData() {
  var start = $('input[name=start]').val();
  var end = $('input[name=end]').val();
  $.ajax({
      url: '/api/get_positions/?start=' + start + '&end=' + end,
      success: function(data) {
        deleteMarkers();
        var point;
        var bounds = new google.maps.LatLngBounds();
        var points = $.parseJSON(data).points
        for (var i = 0; i < points.length; i++) {
          point = points[i];
          var marker = new google.maps.Marker({
            position: new google.maps.LatLng(point['latitude'], point['longitude'])
          });
          markers.push(marker);
          bounds.extend(marker.position);
        }
        showMarkers(map);
        map.fitBounds(bounds);
      },
      error: function() {
        alert("Ruh-roh, we got some sort of error, try retyping the dates?");
      }
  });
}


$(document).ready(function() {
  $('#fullpage').fullpage({
    anchors: ['now', 'previously'],
    scrollBar: true,
    afterLoad: function(anchorLink, index){
        ensureInitialized();
    }
  });
});
