import React, { useState } from "react";
import ReactMapGL, { Source, Layer } from "react-map-gl";

export default function Map() {
  const [viewport, setViewport] = useState({
    width: "100vw",
    height: "100vh",
    latitude: 37.73332,
    longitude: -119.59423,
    zoom: 13
  });

  return (
    <ReactMapGL
      {...viewport}
      mapStyle="https://cdn.jsdelivr.net/gh/nst-guide/osm-liberty-topo@gh-pages/style.json"
      onViewportChange={setViewport}
      mapOptions={{ hash: true }}
    >
      <Source
        id="slope-angle-shading"
        minzoom={0}
        maxzoom={15}
        type="raster"
        tileSize={256}
        tiles={[
          "https://8c51ijx3g1.execute-api.us-east-1.amazonaws.com/production/{z}/{x}/{y}.png"
        ]}
      >
        <Layer
          id="slope-angle-shading-layer"
          type="raster"
          beforeId="building"
        />
      </Source>
    </ReactMapGL>
  );
}
