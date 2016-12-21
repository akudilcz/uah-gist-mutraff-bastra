// This example requires the Drawing library. Include the libraries=drawing
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=drawing">

function initMap() {
  var xmlHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!-- MUTRAFF TAZ-CALC version=\"0.1\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://sumo.dlr.de/xsd/nodes_file.xsd\"> -->\n<mutazs>\n"
  var xmlBody = ""
  var xmlTail = "</mutazs>"
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {
      lng: -3.329860,
      lat: 40.504169
    },
    zoom: 14
  });

  var drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.POLYGON,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
        google.maps.drawing.OverlayType.MARKER,
        google.maps.drawing.OverlayType.CIRCLE,
        google.maps.drawing.OverlayType.POLYGON,
        google.maps.drawing.OverlayType.POLYLINE,
        google.maps.drawing.OverlayType.RECTANGLE
        ],
      },
    markerOptions: {icon: 'images/beachflag.png'},
    polygonOptions: {
      editable: true
    }

  });

  google.maps.event.addListener(map, 'click', function(e) {
    var resultColor = 'red';

    new google.maps.Marker({
      position: e.latLng,
      map: map,
      icon: {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: resultColor,
        fillOpacity: .2,
        strokeColor: 'white',
        strokeWeight: .5,
        scale: 10
      }
    });
  });
  
  drawingManager.setMap(map);

  google.maps.event.addListener(drawingManager, 'overlaycomplete', function(event) {
    event.overlay.set('editable', true);
    // drawingManager.setMap(null);
    // console.log(event.overlay);
  });

  google.maps.event.addListener(drawingManager, 'polygoncomplete', function (polygon) {
    var mutaz_name = prompt("Please enter area name", "Ex: noth-east");
    var coords = (polygon.getPath().getArray());
    var vid = "" // vertex id
    xmlBody += "<mutaz id=\"" + mutaz_name + "\">\n"
    for (var i = 0; i < coords.length; i++) {
      vid = mutaz_name + "-" + i
      xmlBody += "  <vertex id=\"" + vid + "\" x=\"" + coords[i].lng() + "\" y=\"" + coords[i].lat()+"\"/>\n"
    }
    xmlBody +="</mutaz>\n\n"
    xmlModal.innerText = xmlHeader+xmlBody+xmlTail
    modal.style.display = "block" 
});
}
