'use strict'
import { Button, Icon, Spin, Slider, InputNumber, Row, Col, Card } from 'antd';

import "../../utils/Conf.js"


export default class AnalysisBox extends React.Component {
	constructor(props) {
		super(props);
		this.refresh = this.refresh.bind(this);
		this.changeRefreshMaxResults = this.changeRefreshMaxResults.bind(this);
	}

	refresh() {
		this.props.onRefresh();
	}

	changeRefreshMaxResults(value) {
		this.props.onChangeRefreshMaxResults(value);
	}

	render() {
		return (
			<Card title="Refresh" className="refresh-box">
				<div style={{ width: "100%", textAlign: "left", fontSize: 16 }}>Max Number of Return URLs</div>
				<Row gutter={16}>
					<Col span={16}>
						<Slider min={1} max={100} value={this.props.refreshMaxResults} onChange={this.changeRefreshMaxResults} />
					</Col>
					<Col span={3}>
						<InputNumber 
							min={1} 
							max={100} 
							size="large" 
							value={this.props.refreshMaxResults} 
							onChange={this.changeRefreshMaxResults} 
							style={{ width: "80%", marginLeft: "20%" }}
						/>
					</Col>
					<Col span={5}>
						<Button type="primary" size="large" style={{ width: "100%" }} onClick={this.refresh}>
		            		<Icon type="sync" />
		            		Refresh
		          		</Button>
					</Col>
				</Row>
			</Card>
		);
	}
}