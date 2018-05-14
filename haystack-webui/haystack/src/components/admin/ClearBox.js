'use strict'
import { Button, Icon, Spin, Modal } from 'antd';
const confirm = Modal.confirm;

import "../../utils/Conf.js"


export default class ClearBox extends React.Component {
	constructor(props) {
		super(props);
		this.doClear = this.doClear.bind(this);
		this.showDeleteConfirm = this.showDeleteConfirm.bind(this);
	}

	showDeleteConfirm() {
		var doClear = this.doClear;
		confirm({
			title: 'Are you sure to delete all data?',
		    okText: 'Yes',
		    okType: 'danger',
		    cancelText: 'No',
		    onOk() {
		    	doClear();
		    },
		    onCancel() {
		    },
		});
	}

	doClear() {
		this.props.onClear();
	}

	render() {
		return (
			<div>
				<Button type="danger" style={{ height: 60, width: 300, fontSize: 20 }} onClick={this.showDeleteConfirm}>
            		<Icon type="delete" />
            		Delete all data
          		</Button>
			</div>
		);
	}
}