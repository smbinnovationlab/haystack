'use strict';
import { Layout, Input, Avatar, Popover, Button, Menu, Dropdown, Icon } from 'antd';
const { Content, Sider } = Layout;


export default class HomePageHeader extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<Layout style={{ height: '56px', lineHeight: '56px', background: '#fff' }}>
				<Sider width={350} style={{ background: '#fff' }}>
					<img src="/src/pic/asset/haystack.gif" className="header-icon" />
					<div className="header-title">Haystack  SDK</div>
				</Sider>
				<Content style={{ textAlign: 'right', paddingRight: '48px' }}>
				</Content>
			</Layout>
		);
	}
}