'use strict';
import { Layout, Menu, Icon, Spin, message } from 'antd';
const { Header, Content, Footer, Sider } = Layout;

import HomePageHeader from './HomePageHeader.js'
import HomePageTabs from './HomePageTabs.js'
import "../utils/Conf.js"


export default class SdkPage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentMenuItem: "demo",
			uploadPageHeader: "Try the Haystack SDK",
			uploadBoxDisplay: "block",
			maxResults: 20,
			productId: null,
			retDisplay: "none",
			processingDisplay: false,
			retVal: null,
			displayInJson: false
		}
		this.handleClickMenu = this.handleClickMenu.bind(this);
		this.handleChangeMaxResults = this.handleChangeMaxResults.bind(this);
		this.handleDraggerChange = this.handleDraggerChange.bind(this);
		this.handleGetResults = this.handleGetResults.bind(this);
		this.handleDisplayInJson = this.handleDisplayInJson.bind(this);
	}

	handleClickMenu(event) {
		this.setState({
			currentMenuItem: event.key
		});
	}

	handleChangeMaxResults(value) {
		this.setState({
			maxResults: value
		});
	}

	handleDraggerChange(val) {
		this.setState({
			uploadPageHeader: "Results",
			uploadBoxDisplay: "none",
			productId: val,
	    	retDisplay: "block",
	    	processingDisplay: true
		});
	}

	handleGetResults() {
		var retVal = this.state.retVal;
		$.ajax({
			type: "GET", 
			url: serviceUrl + "/api/product?id=" + this.state.productId,
			dataType: "json",
			success: function(data) {
				if (data["status"] === "searching")	return;

				var processingDisplay = true;
				if (data["status"] === "completed")
					processingDisplay = false;

				// var finishedSites = data["results"];
				// for (var i = 0; i < finishedSites.length; i++) {
				// 	var site = finishedSites[i];
				// 	var isNew = true;
				// 	for (var j = 0; j < retVal.length; j++) {
				// 		if (site["id"] == retVal[j]["id"]) {
				// 			isNew = false;
				// 			break;
				// 		}
				// 	}
				// 	if (isNew) {
				// 		retVal.push({
				// 			id: site["id"],
				// 			url: site["url"],
				// 			price: site["target_price"]["value"],
				// 			currency: site["target_price"]["currency"]
				// 		})
				// 	}
				// }

				retVal = data;

				this.setState({
					processingDisplay: processingDisplay,
					retVal: retVal
				});
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				// console.log(XMLHttpRequest.status);
 			// 	console.log(XMLHttpRequest.readyState);
 			// 	console.log(textStatus);
			}.bind(this)
		});
	}

	handleDisplayInJson(checked) {
		this.setState({
			displayInJson: checked
		});
	}

	render() {
		return (
			<Layout>
				<Header className="home-header" style={{ height: '56px', padding: 0, background: '#fff' }}>
					<HomePageHeader />
				</Header>
				<Content style={{ padding: "8px 0", background: '#fff' }}>
					<HomePageTabs
						uploadPageHeader={this.state.uploadPageHeader}
						uploadBoxDisplay={this.state.uploadBoxDisplay}
						maxResults={this.state.maxResults} 
						productId={this.state.productId}
						retDisplay={this.state.retDisplay} 
						processingDisplay={this.state.processingDisplay} 
						retVal={this.state.retVal}
						displayInJson={this.state.displayInJson}
						handleChangeMaxResults={this.handleChangeMaxResults} 
						handleDraggerChange={this.handleDraggerChange} 
						handleGetResults={this.handleGetResults}
						handleDisplayInJson={this.handleDisplayInJson}
					/>
				</Content>
			</Layout>
	  	);
	}
}