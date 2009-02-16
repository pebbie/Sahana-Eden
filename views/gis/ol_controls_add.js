﻿//Controls to add (point/line/polygon) on map but not to create feature in db
//- to be used to locate a single feature from another module.

// Add control to add new Points to the map.
pointControl = new OpenLayers.Control.DrawFeature(featuresLayer, OpenLayers.Handler.Point);
pointControl.featureAdded = shn_gis_map_add_geometry;
map.addControl(pointControl);
// Add control to add new Lines to the map.
lineControl = new OpenLayers.Control.DrawFeature(featuresLayer, OpenLayers.Handler.Path);
lineControl.featureAdded = shn_gis_map_add_geometry;
map.addControl(lineControl);
// Add control to add new Polygons to the map.
polygonControl = new OpenLayers.Control.DrawFeature(featuresLayer, OpenLayers.Handler.Polygon);
polygonControl.featureAdded = shn_gis_map_add_geometry;
map.addControl(polygonControl);

// Start with navigate activated.
// ol_controls_activation.js
shn_gis_map_control_navigate();

function shn_gis_map_add_geometry(feature){
    var fcopy = feature.clone();
    // need for later.
    var fcopygeom = fcopy.geometry.clone();
    var lonlat = fcopy.geometry.getBounds().getCenterLonLat();
    var proj_current = map.getProjectionObject();
    lonlat.transform(proj_current, proj4326);
    var lon_new = lonlat.lon;
    var lat_new = lonlat.lat;
    var wkt_new = fcopy.geometry.transform(proj_current, proj4326).toString();
    var type_new = featureTypeStr(fcopy);
    
    // Update form fields
    var x_gps = document.getElementById("gps_x");
    var y_gps = document.getElementById("gps_y");
    if( x_gps != null && y_gps != null){
        x_gps.value = lon_new;
        y_gps.value = lat_new;
    }

    // store x,y coords in hidden variables named loc_x, loc_y
    // must be set via calling page
    var x_point = document.getElementsByName("loc_x");
    var y_point = document.getElementsByName("loc_y");
    if(x_point != null && y_point != null){
        x_point[0].value = lon_new;
        y_point[0].value = lat_new;
    }
    // store type
    var loc_type = document.getElementsByName("loc_type");
    if(loc_type != null){
        loc_type[0].value = type_new;
    }
    // store wkt value
    var wkt_point = document.getElementsByName("loc_wkt");
    if(wkt_point != null){
        wkt_point[0].value = wkt_new;
    }
    
    // Remove last plot from layer
    featuresLayer.destroyFeatures(featuresLayer.features);
    
    // Add icon.  
    add_Feature(featuresLayer, 'newFeature', fcopygeom, '<?= $icon ?>');
}
