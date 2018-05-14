'use strict';
import { Affix, Layout, Tabs, Spin } from 'antd';
const { Sider } = Layout;
const TabPane = Tabs.TabPane;

import HomePageDashboard from './HomePageDashboard.js'
import HomePageEventsFilterTags from './HomePageEventsFilterTags.js'
import HomePageEventsSortTags from './HomePageEventsSortTags.js'
import HomePageEventsTab from './HomePageEventsTab.js'
import HomePageProductsFilterTags from './HomePageProductsFilterTags.js'
import HomePageProductsCatergories from './HomePageProductsCatergories.js'
import HomePageProductsTab from './HomePageProductsTab.js'


const pageWidth = document.body.clientWidth;


export default class HomePageTabs extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<Tabs defaultActiveKey="dashboard">
				<TabPane tab="DASHBOARD" key="dashboard" style={{ borderTop: "1px solid #d9d9d9", marginTop: "-16px" }}>
					<HomePageDashboard {...this.props} />
				</TabPane>
				<TabPane tab="ACTIVITIES" key="happend" style={{ borderTop: "1px solid #d9d9d9", marginTop: "-16px" }}>
					<Spin spinning={this.props.eventsSpinning} size="large" style={{ width: "auto" }}>
						<Layout style={{ background: '#fff' }}>
							<Sider width={270} style={{ background: '#fff', borderRight: '1px solid #d9d9d9' }}>
								<Affix>
									<HomePageEventsFilterTags {...this.props} />
									<HomePageEventsSortTags {...this.props} />
								</Affix>
							</Sider>
							<HomePageEventsTab {...this.props} />
						</Layout>
					</Spin>
				</TabPane>
				<TabPane tab="ALL PRODUCTS" key="all" style={{ borderTop: "1px solid #d9d9d9",marginTop: '-16px' }}>
					<Spin spinning={this.props.productsSpinning} size="large" style={{ width: "auto" }}>
						<Layout>
							<Sider width={270} style={{ background: '#fff', borderRight: '1px solid #d9d9d9' }}>
								<Affix>
									<HomePageProductsFilterTags {...this.props} />
									<HomePageProductsCatergories {...this.props} />
								</Affix>
							</Sider>
							<HomePageProductsTab {...this.props} />
						</Layout>
					</Spin>
				</TabPane>
			</Tabs>
		);
	}
}