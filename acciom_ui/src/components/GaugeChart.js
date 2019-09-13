import React from 'react';
import Chart from 'react-apexcharts';

function GaugeChart (props) {
	const options = {
		chart: {
			type: 'radialBar',
		},
		plotOptions: {
			radialBar: {
				startAngle: -90,
				endAngle: 90,
				track: {
					background: "#e7e7e7",
					strokeWidth: '97%',
					margin: 5,
					shadow: {
						enabled: true,
						top: 2,
						left: 0,
						color: '#000000',
						opacity: 1,
						blur: 2
					}
				},
				dataLabels: {
					name: {
						show: true
					},
					value: {
						offsetY: 15,
						fontSize: '0px'
					}
				}
			}
		},
		fill: {
			type: 'solid',
			colors: props.color
		},
		series: [props.percentage],
		labels: [props.percentage.toFixed(2) + '%']
	};

	return (
		<div className="row DQIprojectGauge ">  
			<Chart options={options} series={options.series} type="radialBar" width={props.width ? props.width : 200}/>
			<span className={props.class}>{props.name}</span>
		</div>
	);
}

export default GaugeChart;
