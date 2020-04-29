import React, { useState } from "react";
import ReactMapGL, { Source, Layer } from "react-map-gl";

export default function Map() {
  const [viewport, setViewport] = useState({
    width: "100vw",
    height: "100vh",
    latitude: 36.1284,
    longitude: -112.1861,
    zoom: 12
  });

  return (
    <ReactMapGL
      {...viewport}
      mapStyle="https://cdn.jsdelivr.net/gh/nst-guide/osm-liberty-topo@gh-pages/style.json"
      onViewportChange={setViewport}
      mapOptions={{ hash: true }}
    >
      <Source
        id="hillshade"
        minzoom={0}
        maxzoom={15}
        type="raster"
        tileSize={256}
        tiles={[
          "https://us-east-1-lambda.kylebarron.dev/slope/hillshade/{z}/{x}/{y}.png"
        ]}
      >
        <Layer
          id="hillshade-layer"
          type="raster"
          beforeId="building"
          paint={{
            "raster-opacity": 0.6
          }}
        />
      </Source>

      <Source
        id="slope-angle-shading"
        minzoom={0}
        maxzoom={15}
        type="raster"
        tileSize={256}
        tiles={[
          "https://us-east-1-lambda.kylebarron.dev/slope/slope/{z}/{x}/{y}.png"
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
