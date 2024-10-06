import { Container } from '@mui/material';
import React from 'react';

export function ThreeByThreeGrid({ latlng, img: src }) {
    const canvasRef = React.useRef();

    React.useEffect(() => {
        const img = new Image();
        img.src = src;
        console.log(src);
        img.onload = function() {
            console.log(img);
            const context = canvasRef.current.getContext('2d');
            context.drawImage(img, 0, 0);   
        }
        
    }, [src, latlng]);
    return <Container>
        <canvas ref={canvasRef} style={{ width: '300px', height: '300px' }} />
    </Container>
}