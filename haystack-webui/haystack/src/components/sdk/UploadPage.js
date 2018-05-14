import { Icon, Input, Upload, Slider, InputNumber, Row, Col, message, Card } from 'antd';
const Dragger = Upload.Dragger;
const { TextArea } = Input;

import "../../utils/Conf.js"


export default class UploadPage extends React.Component {
	constructor(props) {
		super(props);
		this.onChangeMaxResults = this.onChangeMaxResults.bind(this);
		this.onDraggerChange = this.onDraggerChange.bind(this);
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
		if (processingDisplay === "none" || productId === null)
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
	    	var productId = parseInt(info.file.response);
	    	this.props.handleDraggerChange(productId);
	    } else if (status === 'error') {
	    	message.error(`${info.file.name} file upload failed.`);
	    }
	}

	render() {
		var uploadURL = serviceUrl + "api/upload?max=" + this.props.maxResults;

		const retStyle = { 
			display: this.props.retDisplay, 
			marginTop: 16
		};
		const retVal = this.props.retVal;

		const processingCardStyle = { 
			display: this.props.processingDisplay, 
			marginTop: 16
		};

		return (
			<div className="upload-picture-box" style={{ display: this.props.display }}>
				<Card style={{ background: '#404040' }} noHovering={true}>
					<span style={{ fontSize: 26, color: '#ffffff', lineHeight: 3 }}>Haystack SDK</span>
				</Card>
				<Card style={{ marginTop: 16, textAlign: 'left' }}>
					<span style={{ float: "left", fontSize: 16 }}>Max Sites Amount</span>
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
				</Card>
				<div style={{ marginTop: 16 }}>
					<Dragger 
						height={300} 
						action={uploadURL} 
						onChange={this.onDraggerChange} 
					>
						<p className="ant-upload-drag-icon"><Icon type="inbox" /></p>
						<p className="ant-upload-text">Click or drag picture files to this area to upload</p>
					</Dragger>
				</div>
				<div style={retStyle}>
		  			{retVal.map((val) => {
		  				return (
		  					<Card key={val["id"]} style={{ marginBottom: 16, textAlign: "left", fontSize: 16 }}>
		  						<div style={{ textOverflow: "ellipsis", overflow: "hidden" }}>
		  							<nobr>
		  								<span>{val["currency"]}{" "}{val["price"]}{" "}</span>
		  								<a target="_blank" href={val["url"]}>{" "}{val["url"]}</a>
		  							</nobr>
		  						</div>
		  					</Card>
		  				);
		  			})}
		  		</div>
		  		<Card loading style={processingCardStyle}></Card>
			</div>
		);
	}
}