'use strict'
import { Button, Icon, Spin, Modal } from 'antd';
const confirm = Modal.confirm;

import "../../utils/Conf.js"


export default class BeautifyBox extends React.Component {
	constructor(props) {
		super(props);
		this.doBeautify = this.doBeautify.bind(this);
		this.showConfirm = this.showConfirm.bind(this);
	}

	showConfirm() {
		var doBeautify = this.doBeautify;
		confirm({
			title: 'Are you sure to beautify the data?',
		    okText: 'Yes',
		    cancelText: 'No',
		    onOk() {
		    	doBeautify();
		    },
		    onCancel() {
		    },
		});
	}

	doBeautify() {
		this.props.onBeautify();
	}

	render() {
		return (
			<div>
				<Button type="default" style={{ height: 60, width: 300, fontSize: 20 }} onClick={this.showConfirm}>
            		<Icon type="smile-o" />
            		Beautify data
          		</Button>
			</div>
		);
	}
}