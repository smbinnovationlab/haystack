'use strict';

import "../css/HomePage.css";
import { Card } from 'antd';


export default class DashboardAppearCard extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const events = this.props.events;
		var tempArr = [], arr = [];
		for (var i = 0; i < events.length; i++)
			tempArr.push(events[i]["product_site_id"]);
		for (var i = 0; i < tempArr.length; i++) {
			if (arr.indexOf(tempArr[i]) === -1)
				arr.push(tempArr[i]);
		}
		var sitesNum = arr.length;

		return (
			<div className="dashboard-card">
				<div className="dashboard-card-title">Pages found</div>
				<div className="dashboard-card-body" style={{ height: "112px", textAlign: "center", paddingTop: 16 }}>
					<img src="/src/pic/asset/windows.png" className="dashboard-appear-img" />
					<span className="dashboard-appear-text-large">{sitesNum}</span>
					<span className="dashboard-appear-text-small">sites</span>
				</div>
			</div>
		);
	}
}