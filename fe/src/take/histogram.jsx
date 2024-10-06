import React from 'react';
import { AgCharts } from 'ag-charts-react';

export default function Histogram({ series, srcObj }) {
    const dataSeriesConfig = React.useMemo(() => {
        const dataMap = {};
        const seriesConfig = [];
        const keys = Object.keys(srcObj);

        series.forEach(({ prefix, type }) => {
            keys.forEach((key) => {
                if (key.startsWith(prefix)) {
                    const target = key.replace(prefix, '');
                    let targetObj = dataMap[target];
                    if (!targetObj) {
                        dataMap[target] = targetObj = { name: target };
                    }
                    targetObj[prefix] = +srcObj[key];
                }
            });
            seriesConfig.push({ type, xKey: 'name', yKey: prefix });
        });
        
        return { data: Object.values(dataMap), series: seriesConfig };
    });
    return <AgCharts options={{...dataSeriesConfig, axes: [
        {
            type: 'category',
            position: 'bottom',
            title: {
                text: 'Test histogram'
            }
        },
        {
            type: 'number',
            position: 'left',
            title: {
                text: 'test y'
            },
            // interval: { step: 0.01 }
        },
    ]}} />;
}