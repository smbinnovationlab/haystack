'use strict';
import { Tabs } from 'antd';
const TabPane = Tabs.TabPane;

import DetailPagePriceChart from './DetailPagePriceChart.js'
import DetailPageSitesList from './DetailPageSitesList.js'


export default class DetailPageTabs extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<Tabs 
				className="antd-tabs-bar my-tabs-bar"
				defaultActiveKey="price" 
				style={{ border: 0, borderBottom: 0, textAlign: 'left', marginTop: 24 }}
			>
				<TabPane 
					tab="PRICE HISTORY" 
					key="price" 
					style={{ marginTop: "-16px" }}
				>
					<div className="tab-box">
						<DetailPagePriceChart {...this.props} />
					</div>
				</TabPane>
				<TabPane tab="SITES" key="sites" style={{ marginTop: "-16px" }}>
					<div className="tab-box">
						<DetailPageSitesList {...this.props} />
					</div>
				</TabPane>
			</Tabs>
		);
	}
}