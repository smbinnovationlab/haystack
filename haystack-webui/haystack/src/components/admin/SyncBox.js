import { Button, Card, Form, Input, message } from 'antd';
const FormItem = Form.Item;

import "../../utils/Conf.js"


class SyncBox extends React.Component {
	constructor(props) {
		super(props);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleSubmit(e) {
		e.preventDefault();
		const formData = this.props.form.getFieldsValue();
		this.props.onSync(formData);
	}

	render() {
		const { getFieldDecorator } = this.props.form;
		return (
			<Card title="Sync from Anywhere" className="add-product-box" style={{ display: this.props.display }}>
				<Form style={{ marginTop: 24 }} onSubmit={this.handleSubmit}>
					<FormItem>
						{getFieldDecorator('server')(<Input style={{ width: "50%", minWidth: 200 }} placeholder="SERVER URL" />)}
					</FormItem>
					<FormItem>
						{getFieldDecorator('username')(<Input style={{ width: "50%", minWidth: 200 }} placeholder="LOGIN USERNAME" />)}
					</FormItem>
					<FormItem>
						{getFieldDecorator('password')(<Input style={{ width: "50%", minWidth: 200 }} placeholder="LOGIN PASSWORD" type="password" />)}
					</FormItem>
					<FormItem>
						<Button type="primary" htmlType="submit" style={{ width: "50%", minWidth: 200 }}>Sync</Button>
					</FormItem>
				</Form>
			</Card>
		);
	}
}

export default SyncBox = Form.create()(SyncBox);