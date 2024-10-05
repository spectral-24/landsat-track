import React from 'react';
import {AdvancedMarker, APIProvider, Map} from '@vis.gl/react-google-maps';

export default function MarkerMap() {

    const onMapClick = React.useCallback(({ detail }) => {
        
    }, []);

    return (<APIProvider apiKey={process.env.GOOGLE_MAPS_API_KEY} onLoad={() => console.log('map has loaded')} onError={(err) => console.error('error', err)}>
         <Map
            defaultZoom={13}
            defaultCenter={ { lat: -33.860664, lng: 151.208138 } }
            onClick={}>
        </Map>
    </APIProvider>);
}