'use strict';
import { Layout, Menu, Icon, Spin, message } from 'antd';
const { Header, Content, Footer, Sider } = Layout;

import UploadPage from './UploadPage.js'
import "../../utils/Conf.js"


export default class SdkPage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			productId: null,
			maxResults: 2,
			retDisplay: "none",
			processingDisplay: "none",
			retVal: []
		}
		this.handleChangeMaxResults = this.handleChangeMaxResults.bind(this);
		this.handleDraggerChange = this.handleDraggerChange.bind(this);
		this.handleGetResults = this.handleGetResults.bind(this);
	}

	handleChangeMaxResults(value) {
		this.setState({
			maxResults: value
		});
	}

	handleDraggerChange(val) {
		this.setState({
			productId: val,
	    	retDisplay: "block",
	    	processingDisplay: "block"
		});
	}

	handleGetResults() {
		var retVal = this.state.retVal;
		$.ajax({
			type: "GET", 
			url: serviceUrl + "api/get_product/" + this.state.productId,
			dataType: "json",
			success: function(data) {
				if (data === null)	return;
				var newResults = data;
				for (var i = 0; i < newResults["events"].length; i++) {
					var event = newResults["events"][i];
					var isNew = true;
					for (var j = 0; j < retVal.length; j++) {
						if (event["event_id"] == retVal[j]["id"]) {
							isNew = false;
							break;
						}
					}
					if (isNew) {
						retVal.push({
							id: event["event_id"],
							url: event["full_url"],
							price: event["product_price"],
							currency: event["currency"]
						})
					}
				}

				var processingDisplay = "block";
				if (parseInt(newResults["finished_sites_count"]) === parseInt(newResults["sites_count"]))
					processingDisplay = "none";

				this.setState({
					processingDisplay: processingDisplay,
					retVal: retVal
				});
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	render() {
		return (
			<UploadPage 
				productId={this.state.productId}
				maxResults={this.state.maxResults} 
				retDisplay={this.state.retDisplay} 
				processingDisplay={this.state.processingDisplay} 
				retVal={this.state.retVal}
				handleChangeMaxResults={this.handleChangeMaxResults} 
				handleDraggerChange={this.handleDraggerChange} 
				handleGetResults={this.handleGetResults}
			/>
	  	);
	}
}