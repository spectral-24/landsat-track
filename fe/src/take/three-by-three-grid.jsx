import { Container } from '@mui/material';
import React from 'react';

export function ThreeByThreeGrid({ latlng, img: src }) {
    const canvasRef = React.useRef();

    React.useEffect(() => {
        const img = new Image();
        img.src = src;

        img.onload = function() {
            const [x, y] = [img.naturalWidth / 2, img.naturalHeight / 2];
            const context = canvasRef.current.getContext('2d');
            context.drawImage(img, x, y, 3, 3, 0, 0, 300, 300);

            // Three by three matrix
            context.strokeStyle = 'yellow';
            context.beginPath();
            context.moveTo(100, 0)
            context.lineTo(100, 300)
            context.stroke()

            context.beginPath();
            context.moveTo(200, 0)
            context.lineTo(200, 300)
            context.stroke()

            context.beginPath();
            context.moveTo(0, 100)
            context.lineTo(300, 100)
            context.stroke()

            context.beginPath();
            context.moveTo(0, 200)
            context.lineTo(300, 200)
            context.stroke()
        }
        
    }, [src, latlng]);
    return <Container style={{ width: '300px', height: '300px' }}>
        <canvas ref={canvasRef} width={300} height={300} />
    </Container>
}