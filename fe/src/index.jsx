import React from 'react';
import ReactDOM from 'react-dom/client';
import CssBaseline from '@mui/material/CssBaseline';
import MarkerMap from './map/marker-map';
import Container from '@mui/material/Container';
import './global-style.css';

function App() {
    return <div style={{ height: '100vh', width: '100%' }}>
            <MarkerMap />
        </div>;
}

window.landsappInstall = function install() {
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
};
