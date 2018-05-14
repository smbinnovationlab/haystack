import { Button, Card, Form, Input, message } from 'antd';
const FormItem = Form.Item;

import "../../utils/Conf.js"


class AddProductBox extends React.Component {
	constructor(props) {
		super(props);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleSubmit(e) {
		e.preventDefault();
		console.log(adminUrl);
		const formData = this.props.form.getFieldsValue();
		$.ajax({
			type: "POST", 
			url: adminUrl + "add",
			data: formData, 
			dataType: "text",
			success: function() {
				message.success('Added successfully');
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	render() {
		const { getFieldDecorator } = this.props.form;
		return (
			<Card title="Product Information" className="add-product-box" style={{ display: this.props.display }}>
				<Form style={{ marginTop: 24 }} onSubmit={this.handleSubmit}>
					<FormItem>
						{getFieldDecorator('name')(<Input style={{ width: "50%", minWidth: 200 }} placeholder="Product Name" />)}
					</FormItem>
					<FormItem>
						{getFieldDecorator('price')(<Input style={{ width: "50%", minWidth: 200 }} placeholder="Product Price" />)}
					</FormItem>
					<FormItem>
						{getFieldDecorator('currency')(<Input style={{ width: "50%", minWidth: 200 }} placeholder="Currency" />)}
					</FormItem>
					<FormItem>
						{getFieldDecorator('sku_id')(<Input style={{ width: "50%", minWidth: 200 }} placeholder="SKU ID" />)}
					</FormItem>

					<FormItem>
						<Button type="primary" htmlType="submit" style={{ width: "50%", minWidth: 200 }}>Add Product</Button>
					</FormItem>
				</Form>
			</Card>
		);
	}
}

export default AddProductBox = Form.create()(AddProductBox);