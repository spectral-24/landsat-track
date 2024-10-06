import React from 'react';
import ReactDOM from 'react-dom/client';
import MarkerMap from './map/marker-map';
import {
    createBrowserRouter,
    RouterProvider,
  } from "react-router-dom";
import './global-style.css';
import ImageDisplay from './take/image-display';


const router = createBrowserRouter([
    { path: '/', element: <div style={{ height: '100vh', width: '100%' }}>
        <MarkerMap />
    </div>},
    { path: '/take/:prefix', element: <ImageDisplay /> }
])
function App() {
    return <RouterProvider router={router} />;
}

window.landsappInstall = function install() {
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
};
