'use strict';

import { Row, Col, Spin } from 'antd';

import "../css/HomePage.css";
import DashboardAppearCard from './DashboardAppearCard.js'
import DashboardFavouritesCard from './DashboardFavouritesCard.js'
import DashboardHappendCard from './DashboardHappendCard.js'
import DashboardPagesCard from './DashboardPagesCard.js'
import DashboardWarningsCard from './DashboardWarningsCard.js'


// const pageHeight = document.documentElement.clientHeight;
const pageHeight = document.body.clientHeight


export default class HomePageDashboard extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="dashboard-box" style={{ minHeight: pageHeight }}>
				<Row gutter={8}>
					<Col sm={24} md={12} style={{ margin: "32px 0" }}>
						<Spin spinning={this.props.eventsSpinning} size="large" style={{ width: "auto" }}>
							<DashboardHappendCard {...this.props} />
						</Spin>
					</Col>
					<Col sm={24} md={6} style={{ margin: "32px 0" }}>
						<Spin spinning={this.props.crawledSitesSpinning} size="large" style={{ width: "auto" }}>
							<DashboardPagesCard {...this.props} />
						</Spin>
						<Spin spinning={this.props.eventsSpinning} size="large" style={{ width: "auto" }}>
							<DashboardAppearCard {...this.props} />
						</Spin>
					</Col>
					<Col sm={24} md={6} style={{ margin: "32px 0" }}>
						<Spin spinning={this.props.eventsSpinning} size="large" style={{ width: "auto" }}>
							<DashboardWarningsCard {...this.props} />
						</Spin>
					</Col>
					<div className="dashboard-title">FAVORITES</div>
					<Col sm={24} style={{ marginBottom: "32px" }}>
						<Spin spinning={this.props.productsSpinning} size="large" style={{ width: "auto" }}>
							<DashboardFavouritesCard {...this.props} />
						</Spin>
					</Col>
				</Row>
			</div>
		);
	}
}