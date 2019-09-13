import React, { Component } from 'react';
import Slider from "react-slick";
import { connect } from 'react-redux';
import DonutChart from '../components/DonutChart';

class ProjectChartList extends Component {
		
	constructor(props) {
		super(props);
		this.next = this.next.bind(this);
		this.previous = this.previous.bind(this);
	}

	next() {
		this.slider.slickNext();
	}

	previous() {
		this.slider.slickPrev();
	}
	
	render() {

		// this.colorsArray = [
		// 	['#E74B56', '#cc9900'],
		// 	['#E74B56', '#ffddff'],
		// 	['#E74B56', '#ff00dd'],
		// 	['#E74B56', '#ff00aa'],
		// ];

		this.getDonutCharts = () => {
			let elements = '';

			const chartList = this.props.projects.map((item, index) => {
				return (<DonutChart key={ index } chartindex={index} chartData={item} />);
			});
			
			if (this.props.projects.length > 4 ) {
				elements = (
					<div>
						<i className="previousArrow fas fa-arrow-circle-left fa-2x" style={{color: 'green'}} onClick={this.previous}></i>
						<Slider ref={c => (this.slider = c)} {...settings}>
							{ chartList }
						</Slider>
						<i className="nextArrow fas fa-arrow-circle-right fa-2x" style={{color: 'green'}} onClick={this.next}></i>
					</div>
				);
			} else {
				elements = chartList;
			}
			
			return elements;
		};

		const settings = {
			dots: false,
			infinite: true,
			speed: 500,
			slidesToShow: 4,
			slidesToScroll: 1
		};

		return (
			<div className="row projectList">
				<div className="main_titles QLindex-title">Quality Index</div>
				{ this.getDonutCharts() }
			</div>
		);
	}
}

const mapStateToProps = state => {
	return {
		projects: state.dashboardData.orgDataQuality && state.dashboardData.orgDataQuality.projects?state.dashboardData.orgDataQuality.projects: []
	};
};

export default connect(mapStateToProps)(ProjectChartList);
