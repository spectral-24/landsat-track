import React, { useEffect } from 'react';
import { Button, CircularProgress, Container, CssBaseline, Stack, Typography } from '@mui/material';
import { useParams, redirect, useNavigate } from 'react-router';
import BoundaryMap from '../map/bundary-map';
import { ArrowBackSharp } from '@mui/icons-material';
import api from '../api/api';
import DownloadableTable from './downloadable-table';
import Histogram from './histogram';
import { ThreeByThreeGrid } from './three-by-three-grid';

const STATIC_ASSETS_URL = `${process.env.API_URL}/static`;

function getJsonFile(file) {
    return api.getStatic(`${file}.json`)
            .then((r) => r.json());
}

export default function ImageDisplay(){
    const params = useParams();
    const navigate = useNavigate();

    const onGoBack = React.useCallback(() => {
        navigate('/');
    }, []);

    const [takeData, setTakeData] = React.useState();
    const [landsatMetadata, setLandsatMetadata] = React.useState();

    useEffect(() => {
        if (params?.prefix) {
            getJsonFile(params.prefix)
            .then((json) => {
                const { geometry, properties } = json;
                setTakeData({
                    boundaries: geometry.coordinates[0],
                    properties
                });
            });

            getJsonFile(`${params.prefix}_mtl`)
            .then(json => {
                const { LANDSAT_METADATA_FILE: fileContents } = json;
                setLandsatMetadata(fileContents);
            });
        }
    }, [!!params?.prefix]);

    if (!params?.prefix) {
        return redirect('/');
    }


    const { prefix } = params;
    return <CssBaseline>
        <Container>
            <Button onClick={onGoBack}>
                <ArrowBackSharp /> Go Back
            </Button>
        </Container>
        <Container style={{ justifyContent: 'center' }}>
            <Typography component="h1" fontWeight={900}>Landsat take for your specified location</Typography>
        </Container>
        <Container>
            <Stack spacing={2} direction="row">
                <Container>
                    {!!takeData?.boundaries && <BoundaryMap boundaries={takeData.boundaries} />}
                    {!takeData && <CircularProgress />}
                </Container>
                <Container>
                    <img style={{ width: '100%' }} src={`${STATIC_ASSETS_URL}/${prefix}.jpg`} />
                </Container>
            </Stack>
        </Container>
        <Container>
            <Stack spacing={2} direction='row'>
                <Container>
                    <Typography fontWeight={500}>Metadata from acquisition</Typography>
                    {!takeData && <CircularProgress />}
                    {!!takeData && <DownloadableTable entries={Object
                            .entries(takeData.properties)
                            .filter(([_, value]) => typeof value !== 'object')} />}
                    {!landsatMetadata && <CircularProgress />}
                    {!!landsatMetadata && <ThreeByThreeGrid img={`${STATIC_ASSETS_URL}/${prefix}.jpg`} latLng={{ lat: 1, lng: 1}} />}
                </Container>
                <Container>
                    <Typography fontWeight={500}>Surface Reflectance and Surface Temperature Data</Typography>
                    {!landsatMetadata && <CircularProgress />}
                    {!!landsatMetadata && <DownloadableTable entries={Object.entries(landsatMetadata.LEVEL2_SURFACE_REFLECTANCE_PARAMETERS)} />} 
                </Container>
            </Stack>
        </Container>
        <Container>
            {!landsatMetadata && <CircularProgress />}
            {landsatMetadata && <Histogram series={[{ prefix: 'REFLECTANCE_MAXIMUM_', type: 'line' },
                 { prefix: 'REFLECTANCE_MINIMUM_', type: 'line' }]} srcObj={landsatMetadata.LEVEL2_SURFACE_REFLECTANCE_PARAMETERS} />}
        </Container>

    </CssBaseline>;
}