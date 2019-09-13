import React, { Component } from 'react';
import { connect } from 'react-redux';
import { getDQIprojectDetails } from '../actions/dashboardActions';

import Chart from 'react-apexcharts';

class DonutChart extends Component {
	render() {
		this.options = {
			chart: {
				height: 220,
				type: 'radialBar',
			},
			series: [this.props.chartData.project_dqi_percentage.toFixed(2)],
			labels: ['DQI'],
			colors: ['#E74B56'],
			plotOptions: {
				radialBar: {
					dataLabels: {
						showOn: "always",
						name: {
							offsetY: -5,
							show: true,
							color: "#888",
							fontSize: "15px",
						},
						value: {
							color: "#111",
							fontSize: "15px",
							show: true,
							offsetY: 5
						}
					}
				}
			}
		}
		return (
			<div className="donut">
				<Chart options={this.options} series={this.options.series} colors={this.options.colors} type="radialBar" width="220" />
				<span className="chartProjectName">{this.props.chartData.project_name.split(" ")[0]}</span>
			</div>
		);
	}
}

const mapDispatchToProps = (dispatch) => ({
	getDQIprojectDetails: (data) => dispatch(getDQIprojectDetails(data))
});

export default connect(null, mapDispatchToProps)(DonutChart);

