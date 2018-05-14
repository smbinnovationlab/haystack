'use strict';
import { Affix, Layout, Tabs, Spin, Menu } from 'antd';
const { Sider } = Layout;
const TabPane = Tabs.TabPane;

import UploadPage from './UploadPage.js'
import ApiPage from './ApiPage.js'


const pageWidth = document.body.clientWidth;


export default class HomePageTabs extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<Tabs defaultActiveKey="demo" style={{ textAlign: "left" }}>
				<TabPane tab="DEMO" key="demo" style={{ borderTop: "1px solid #d9d9d9", marginTop: "-16px" }}>
					<UploadPage {...this.props} />
				</TabPane>
				<TabPane tab="REFERENCE" key="reference" style={{ borderTop: "1px solid #d9d9d9", marginTop: "-16px" }}>
					<ApiPage />
				</TabPane>
			</Tabs>
		);
	}
}