import React from 'react';
import {Marker, APIProvider, Map} from '@vis.gl/react-google-maps';
import CreateMarkerDialog from '../dialogs/create-marker';


export default function MarkerMap() {
    const [savedMarkers, setSavedMarkers] = React.useState([]);
    const [currentSelected, setCurrentSelected] = React.useState();

    const onMapClick = React.useCallback(({ detail }) => {
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
            </Map>
        </APIProvider>
    </React.Fragment>;
}