import React from 'react';

import {Marker, APIProvider, Map, useMap, useMapsLibrary} from '@vis.gl/react-google-maps';

function BoundaryMap({ boundaries }) {

    const map = useMap('boundary-map');
    const mapLibrary = useMapsLibrary('maps');

    React.useEffect(() => {
        if (mapLibrary && map) {
            new mapLibrary.Polygon({
                strokeColor: "#FF0000",
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: "#FF0000",
                fillOpacity: 0.35,
                paths: boundaries.map(([lng, lat]) => ({ lat, lng })),
                map
            });
        }
    }, [boundaries, !!mapLibrary && !!map]);

    return <Map
        id="boundary-map"
        defaultZoom={5}
        defaultCenter={ { lat: boundaries[0][1], lng: boundaries[0][0] } }
        disableDefaultUI={true}
        gestureHandling={'none'}
        ></Map>;
}

export default function BoundaryMapWrapper({ boundaries }) {
    const [loaded, setLoaded] = React.useState(false);
    const ref = React.useRef();

    return <APIProvider apiKey={process.env.GOOGLE_MAPS_API_KEY} onLoad={() => setLoaded(true)} onError={(err) => console.error('error', err)}>
            <BoundaryMap boundaries={boundaries} />
        </APIProvider>;
}