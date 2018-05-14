'use strict';
import { Modal, Button, Input, Spin } from 'antd';


export default class PopSyncBox extends React.Component {
	constructor(props) {
		super(props);
		this.sync = this.sync.bind(this);
		this.cancel = this.cancel.bind(this);
		this.changeInput = this.changeInput.bind(this);
	}

	sync() {
		this.props.onSync();
	}

	cancel() {
		this.props.hidePopSyncBox();
	}

	changeInput(e) {
		this.props.onChangeInput(e.target.id, e.target.value);
	}

	render() {
		return (
	        <Modal 
	        	title="Sync" 
	        	okText="Sync" 
	        	cancelText="Cancel" 
	        	onOk={this.sync} 
	        	onCancel={this.cancel} 
	        	visible={this.props.popSyncBoxVisible}
	        	width={500} 
	        >
	        	<Spin spinning={this.props.popSyncSpinning} size="large" style={{ width: "auto" }}>
	        	<div style={{ width: 468 }}>
					<Input id="server" size="large" placeholder="SERVER URL" 
						value={this.props.anywhereServerUrl} onChange={this.changeInput} />
					<Input id="username" size="large" placeholder="LOGIN USERNAME" style={{ marginTop: 16 }} 
						value={this.props.anywhereLoginUsername} onChange={this.changeInput} />
					<Input id="password" size="large" placeholder="LOGIN_PASSWORD" type="password" style={{ marginTop: 16 }} 
						value={this.props.anywhereLoginPassword} onChange={this.changeInput} />
				</div>
				</Spin>
	        </Modal>
		);
	}
}