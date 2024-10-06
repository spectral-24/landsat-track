import { Download } from '@mui/icons-material';
import { Button } from '@mui/material';
import React from 'react';
import { mkConfig, generateCsv, download } from 'export-to-csv';

const config = mkConfig({ useKeysAsHeaders: true });
export default function DownloadableTable({ entries }) {
    // TODO: Take a title and download the file with said title
    const onCSVDownload = React.useCallback(() => {
        const toExport = Object.assign({}, ...entries.map(([key, value]) => ({ [key]: value })));
        const csv = generateCsv(config)([toExport]);
        download(config)(csv);
    }, [entries]);

    return <table style={{ width: '100%' }}>
        <thead>
        <tr>
            <th>
                Field
            </th>
            <th>
                Value
            </th>
        </tr>
        </thead>
        <tbody>
        {entries.map(([key, value]) => <tr key={key}>
                <td>{key}</td>
                <td>{value}</td>
        </tr>)}
        <tr>
            <td colSpan="2"><Button onClick={onCSVDownload} style={{ width: '100%' }}>
               <Download /> Download as CSV
            </Button></td>
        </tr>
        </tbody>
    </table>;
}