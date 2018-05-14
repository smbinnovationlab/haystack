'use strict';
import { Modal, Button, Input, Slider, InputNumber, Row, Col } from 'antd';


export default class PopSettingBox extends React.Component {
	constructor(props) {
		super(props);
		this.ok = this.ok.bind(this);
		this.cancel = this.cancel.bind(this);
		this.changeMaxSyncResults = this.changeMaxSyncResults.bind(this);
	}

	ok() {
		this.props.hidePopSettingBox();
	}

	cancel() {
		this.props.hidePopSettingBox();
	}

	changeMaxSyncResults(value) {
		this.props.onChangeMaxSyncResults(value);
	}

	render() {
		return (
	        <Modal 
	        	title="Setting" 
	        	okText="OK" 
	        	cancelText="Cancel" 
	        	onOk={this.ok} 
	        	onCancel={this.cancel} 
	        	visible={this.props.popSettingBoxVisible}
	        	width={500} 
	        >
	        	<span style={{ float: "left", fontSize: 16 }}>Max Number of Return URLs</span>
	        	<Row gutter={0}>
					<Col span={20}>
						<Slider min={1} max={100} value={this.props.maxSyncResults} onChange={this.changeMaxSyncResults} />
					</Col>
					<Col span={4}>
						<InputNumber 
							min={1} 
							max={100} 
							value={this.props.maxSyncResults} 
							onChange={this.changeMaxSyncResults} 
							style={{ width: "80%", marginLeft: "20%" }}
						/>
					</Col>
				</Row>
	        </Modal>
		);
	}
}