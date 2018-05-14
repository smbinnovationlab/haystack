import { Icon, Input, Upload, Slider, InputNumber, Row, Col, message } from 'antd';
const Dragger = Upload.Dragger;
const { TextArea } = Input;

import "../../utils/Conf.js"


export default class UploadPictureBox extends React.Component {
	constructor(props) {
		super(props);
		this.onChangeMaxResults = this.onChangeMaxResults.bind(this);
		this.onDraggerChange = this.onDraggerChange.bind(this);
	}

	onChangeMaxResults(value) {
		this.props.handleChangeMaxResults(value);	
	}

	onDraggerChange(info) {
	    const status = info.file.status;
	    if (status === 'done') {
	    	message.success(`${info.file.name} file uploaded successfully.`);
	    	var response = info.file.response[0];
	    	var val = {
	    		name: response["name"],
	    		urls: response["urls"]
	    	};
	    	var newVal = this.props.retVal;
	    	newVal.push(val);
	    	this.props.handleDraggerChange(newVal);
	    } else if (status === 'error') {
	    	message.error(`${info.file.name} file upload failed.`);
	    }
	}

	render() {
		var uploadURL = adminUrl + "upload_save?max=" + this.props.maxResults;

		const retStyle = { display: this.props.retDisplay, marginTop: 24 };
		const retVal = this.props.retVal;
		var retValue = [];
		for (var i = 0; i < retVal.length; i++)
		{
			var temp = retVal[i];
			var str = "";
			for (var j = 0; j < temp["urls"].length; j++)
			{
				str += temp["urls"][j] + "\n";
			}
			retValue.push({
				id: i,
				name: temp["name"],
				urls: str
			});
		}

		return (
			<div className="upload-picture-box" style={{ display: this.props.display }}>
				<span style={{ float: "left", fontSize: 16 }}>Max Number of Return URLs</span>
				<Row gutter={0}>
					<Col span={21}>
						<Slider min={1} max={100} value={this.props.maxResults} onChange={this.onChangeMaxResults} />
					</Col>
					<Col span={3}>
						<InputNumber 
							min={1} 
							max={100} 
							value={this.props.maxResults} 
							onChange={this.onChangeMaxResults} 
							style={{ width: "80%", marginLeft: "20%" }}
						/>
					</Col>
				</Row>
				<div style={{ marginTop: 16 }}>
					<Dragger height={400} action={uploadURL} onChange={this.onDraggerChange}>
						<p className="ant-upload-drag-icon"><Icon type="inbox" /></p>
						<p className="ant-upload-text">Click or drag picture files to this area to upload</p>
						<p className="ant-upload-hint">Please add product first, then rename the picture file to the same name as the product name</p>
					</Dragger>
				</div>
				<div style={retStyle}>
		  			{retValue.map((val) => {
		  				return (
		  					<div key={val["id"]} style={{ marginBottom: 16 }}>
		  						<h2>{val["name"]}</h2>
		  						<TextArea autosize value={val["urls"]}/>
		  					</div>
		  				);
		  			})}
		  		</div>
			</div>
		);
	}
}