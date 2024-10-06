import React from 'react';
import {Marker, APIProvider, Map} from '@vis.gl/react-google-maps';
import CreateMarkerDialog from '../dialogs/create-marker';

const markers = "1.4502983613597,-65.1409182193289 1.42277780969893,-65.1752813002244 1.39273,-65.2128 1.38996600919357,-65.2123830100401 -2.2834,-64.6582 -2.24969123865004,-64.622025165661 -0.988767051978717,-63.268854009554 -0.95778,-63.2356 2.55222484611702,-63.7619738055709 2.5544,-63.7623 2.52702411735118,-63.7964824423305 2.49710264743922,-63.8338433900242 1.4502983613597,-65.1409182193289".split(' ').map(v => v.split(',').reverse().map(n => +n));

export default function MarkerMap() {
    const [savedMarkers, setSavedMarkers] = React.useState([]);
    const [currentSelected, setCurrentSelected] = React.useState();

    const onMapClick = React.useCallback(({ detail }) => {
        // console.log(detail);
        setCurrentSelected(detail.latLng);
    }, []);

    return <React.Fragment>
        <CreateMarkerDialog 
            onClose={() => setCurrentSelected()} 
            position={currentSelected}
        />
        <APIProvider apiKey={process.env.GOOGLE_MAPS_API_KEY} onLoad={() => console.log('map has loaded')} onError={(err) => console.error('error', err)}>
            <Map
                id="marker-map"
                defaultZoom={10}
                defaultCenter={ { lat: -33.860664, lng: 151.208138 } }
                onClick={onMapClick}>
                    {markers.map(([lng, lat]) => <Marker position={{ lat, lng}} />)}
            </Map>
        </APIProvider>
    </React.Fragment>;
}