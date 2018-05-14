'use strict';
import { Layout, Row, Col } from 'antd';
const { Header, Content, Sider } = Layout;

import HomePageHeader from './HomePageHeader.js'
import HomePageTabs from './HomePageTabs.js'

export default class HomePage extends React.Component {
	constructor(props) {
		super(props);
	}

	componentDidMount() {
		window.location = "http://www.baidu.com/";
	}

	render() {
		return (
			<h1>Redirecting...</h1>
		);
	}
}