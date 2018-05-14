'use strict';
import { Layout, Input, Avatar, Popover, Button, Menu, Dropdown, Icon } from 'antd';
const { Content, Sider } = Layout;
const Search = Input.Search;

import PopSyncBox from './PopSyncBox.js'
import PopSettingBox from './PopSettingBox.js'
import "../css/HomePage.css";
import "../css/ModifiedAntd.css";


export default class HomePageHeader extends React.Component {
	constructor(props) {
		super(props);
		this.handleClickMenu = this.handleClickMenu.bind(this);
	}

	handleClickMenu(e) {
		if (e.key === "sync")
			this.props.showPopSyncBox();
		else if (e.key === "setting") {
			this.props.showPopSettingBox();
		}
	}

	render() {
		const menu = (
			<Menu className="header-pop-menu" onClick={this.handleClickMenu}>
				<div className="header-pop-info">
					<Avatar icon="user" style={{ backgroundColor: "#37474f", float: "left", margin: "4px 16px 0 0" }} />
					<div>
						<span className="header-pop-info-name">Peter<br/></span>
						<span className="header-pop-info-email">PeterXXX@gmail.com</span>
					</div>
				</div>
		    	<Menu.Item key="account" className="header-pop-menu-item" disabled>
		    		<Icon type="team" />
		    		<span style={{ marginLeft: 8 }}>Switch account</span>
		    	</Menu.Item>
		    	<Menu.Item key="sync" className="header-pop-menu-item">
		    		<Icon type="sync" />
		    		<span style={{ marginLeft: 8 }}>Sync</span>
		    	</Menu.Item>
		    	<Menu.Item key="setting" className="header-pop-menu-item">
		    		<Icon type="setting" />
		    		<span style={{ marginLeft: 8 }}>Setting</span>
		    	</Menu.Item>
		    	<Menu.Item key="logout" className="header-pop-menu-item" disabled>
		    		<Icon type="logout" />
		    		<span style={{ marginLeft: 8 }}>Log out</span>
		    	</Menu.Item>
		  	</Menu>
		);
		return (
			<Layout style={{ height: '56px', lineHeight: '56px', background: '#fff' }}>
				<Sider width={350} style={{ background: '#fff' }}>
					<img src="/src/pic/asset/haystack.gif" className="header-icon" />
					<div className="header-title">Product  Haystack</div>
				</Sider>
				<Content style={{ textAlign: 'right', paddingRight: '48px' }}>
					<Search className="header-search-box" placeholder="Search..." disabled={true} />
					<Dropdown overlay={menu} trigger={['click']}>
						<div className="header-avatar">
							<Avatar icon="user" style={{ backgroundColor: "#37474f", cursor: "pointer" }}/>
						</div>
					</Dropdown>
				</Content>
				<PopSyncBox {...this.props} />
				<PopSettingBox {...this.props} />
			</Layout>
		);
	}
}