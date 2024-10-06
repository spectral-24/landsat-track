import React from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, FormControl, FormControlLabel, FormGroup, InputLabel, MenuItem, Select, Stack, TextField, Typography } from '@mui/material';
import Slider from '@mui/material/Slider';
import CloudOff from '@mui/icons-material/CloudOff';
import Cloud from '@mui/icons-material/Cloud';
import Api from '../api/api';

export default function CreateMarkerDialog({ onClose, onSave, position }) {

    const [params, setParams] = React.useState({})
    const [error, setError] = React.useState();

    const onParamChange = React.useCallback((evt) => {
        const { target } = evt;
        const { name, value } = target;
        setParams((params) => ({ ...params, [name]: value }));
    }, [setParams]);

    const onDialogSave = React.useCallback(() => {
        const P = Api.post('/create-registration', {
            latlng: { lat: position.lat, lng: position.lng },
            ...params
        });
        P.then(() => {
            onSave();
        });
        P.catch((err) => {
            setError(err);
        })
    }, [position, params]);

    return <Dialog open={!!position}>
        <DialogTitle>Create a Point of Interest</DialogTitle>
        <DialogContent>
            <Typography>
                When the Landsat passes over this location, you will be notified based on the settings
                you enter below. You will need to define the expected lead time, cloud coverage and 
                where to reach out for you.
            </Typography>
            <FormGroup>
                    <Stack spacing={2} direction="row" sx={{ alignItems: 'center', mb: 1 }}>
                        <CloudOff />
                        <Slider name='cloud_coverage_result' aria-label="Volume" valueLabelDisplay='auto' onChange={onParamChange} />
                        <Cloud />
                    </Stack>
                    <Stack spacing={2} direction="column" sx={{ alignItems: 'center', mb: 1 }}>
                        <FormControl fullWidth>
                            <InputLabel labelId='selectLabel'>Lead Time</InputLabel>
                            <Select 
                                name='lead_time'
                                labelId='selectLabel'
                                onChange={onParamChange}
                            >
                                <MenuItem value={30*60}>30 min</MenuItem>
                                <MenuItem value={45*60}>45 min</MenuItem>
                            </Select>
                        </FormControl>
                        <FormControl fullWidth>
                            <TextField name='email' label="Email Address" placeholder='Fill if you want email notifications' onChange={onParamChange} />
                        </FormControl>
                        <FormControl fullWidth>
                            <TextField name='phone' label="Phone Number" placeholder='Fill if you want SMS notifications' onChange={onParamChange} />
                        </FormControl>
                    </Stack>                        
            </FormGroup>
        </DialogContent>
        <DialogActions>
            <Button onClick={onClose}>Cancel</Button>
            <Button onClick={onDialogSave}>Save</Button>
        </DialogActions>
    </Dialog>;
}