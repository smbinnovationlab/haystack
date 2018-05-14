import { Icon, Input, Upload, Slider, InputNumber, Row, Col, message, Card, Spin, Switch, Progress } from 'antd';
const Dragger = Upload.Dragger;
const { TextArea } = Input;

import "../utils/Conf.js"


export default class UploadPage extends React.Component {
	constructor(props) {
		super(props);
		this.onChangeMaxResults = this.onChangeMaxResults.bind(this);
		this.onDraggerChange = this.onDraggerChange.bind(this);
		this.onDisplayInJson = this.onDisplayInJson.bind(this);
	}

	componentDidMount() {
		this.intervalID = setInterval(
			() => this.getResults(), 5000
		);
	}

	componentWillUnmount() {
		clearInterval(this.intervalID);
	}

	getResults() {
		var productId = this.props.productId;
		var processingDisplay = this.props.processingDisplay;
		if (processingDisplay === false || productId === null)
			return;
		else
			this.props.handleGetResults();
	}

	onChangeMaxResults(value) {
		this.props.handleChangeMaxResults(value);	
	}

	onDraggerChange(info) {
	    const status = info.file.status;
	    if (status === 'done') {
	    	message.success(`${info.file.name} file uploaded successfully.`);
	    	var productId = info.file.response.id;
	    	this.props.handleDraggerChange(productId);
	    } else if (status === 'error') {
	    	message.error(`${info.file.name} file upload failed.`);
	    }
	}

	onDisplayInJson(checked) {
		this.props.handleDisplayInJson(checked);
	}

	render() {
		var uploadURL = serviceUrl + "/api/upload?max=" + this.props.maxResults;

		const retStyle = { 
			display: this.props.retDisplay, 
			marginTop: 16
		};

		const displayInJson = this.props.displayInJson;
		const retVal = this.props.retVal;
		var retValInJson = "";
		var retValNotInJson = [];
		var uploadResult = null;
		if (retVal != null) {
			if (displayInJson) {
				var retValJsonStr = JSON.stringify(retVal, null, 2);
				uploadResult = (
					<div className="upload-result-json" style={{ marginTop: 40 }}>
						<Highlight className="json">
							{retValJsonStr}
						</Highlight>
					</div>
				);
			} else {
				for(var i = 0; i < retVal.results.length; i++) {
					var tempVal = retVal.results[i];
					retValNotInJson.push({
						id: tempVal.id,
						url: tempVal.url,
						price: tempVal.target_price.value,
						currency: tempVal.target_price.currency
					});
				}
				uploadResult = (
					<div style={{ marginTop: 40 }}>
						{retValNotInJson.map((val) => {
			  				return (
		  						<div className="upload-result-line" key={val["id"]}>
									<nobr>
										<span>{val["currency"]}&nbsp;&nbsp;{val["price"]}&nbsp;&nbsp;</span>
										<a target="_blank" href={val["url"]}>{val["url"]}</a>
									</nobr>
		  						</div>
			  				);
			  			})}
		  			</div>
				);
			}
		}

		const processingCardStyle = { 
			display: this.props.processingDisplay, 
			marginTop: 16
		};


		return (
			<div className="upload-page">
				<h1 className="upload-page-header">{this.props.uploadPageHeader}</h1>
				<div className="upload-picture-box" style={{ marginTop: 16, display: this.props.uploadBoxDisplay }}>
					<Dragger 
						height={250} 
						action={uploadURL} 
						onChange={this.onDraggerChange} 
					>
						<p className="ant-upload-drag-icon"><Icon type="picture" /></p>
						<p className="ant-upload-text">Click or drag picture files to this area to upload</p>
					</Dragger>
				</div>

				<div className="upload-image-box">
					<img 
						src={serviceUrl + "/api/image?id=" + this.props.productId} 
						width="100%"
						className="upload-image" 
						style={retStyle}
					/>	
				</div>
				<Card className="upload-result-box" style={retStyle}>
					<div>
						<div className="upload-result-switch">
							Display in JSON
							<Switch	
								defaultChecked={false}
								checkedChildren={<Icon type="check" />} 
								unCheckedChildren={<Icon type="cross" />} 
								onChange={this.onDisplayInJson}
								style={{ marginLeft: 16 }}
							/>
						</div>
						<Spin spinning={this.props.processingDisplay} className="upload-result-spining" />
					</div>

		  			{uploadResult}
		  		</Card>
			</div>
		);
	}
}