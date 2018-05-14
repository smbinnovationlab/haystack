'use strict';
import { Layout, Menu, Icon, Spin, message } from 'antd';
const { Header, Content, Footer, Sider } = Layout;

import AddProductBox from './AddProductBox.js'
import UploadPictureBox from './UploadPictureBox.js'
import AnalysisBox from './AnalysisBox.js'
import AnalysisResult from './AnalysisResult.js'
import RefreshBox from './RefreshBox.js'
import ClearBox from './ClearBox.js'
import BeautifyBox from './BeautifyBox.js'
import SyncBox from './SyncBox.js'
import "../../utils/Conf.js"
import "../../css/Admin.css"


const pageHeight = window.screen.height;


export default class HomePage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			displayStatus: ["none", "none", "none", "block", "none", "none", "none"],
			maxResults: 2,
			retDisplay: "none",
			retVal: [],
			targetKeys: [],
    		selectedKeys: [],
    		analysisResult: [],
    		spinning: false,
    		refreshSpinning: false,
    		refreshMaxResults: 2,
    		clearSpinning: false,
    		beautifySpinning: false,
    		syncSpinning: false
		}
		this.handleClickMenuItem = this.handleClickMenuItem.bind(this);
		this.handleChangeMaxResults = this.handleChangeMaxResults.bind(this);
		this.handleDraggerChange = this.handleDraggerChange.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.handleChangeSelect = this.handleChangeSelect.bind(this);
		this.handleAnalysis = this.handleAnalysis.bind(this);
		this.handleRefresh = this.handleRefresh.bind(this);
		this.handleClear = this.handleClear.bind(this);
		this.handleBeautify = this.handleBeautify.bind(this);
		this.handleSync = this.handleSync.bind(this);
		this.handleChangeRefreshMaxResults = this.handleChangeRefreshMaxResults.bind(this);
	}

	handleClickMenuItem(e) {
		var newDisplayStatus = [];
		for (var i = 1; i <= 7; i++) {
			if (i == e["key"])
				newDisplayStatus.push("block");
			else
				newDisplayStatus.push("none");
		}
		this.setState({
			displayStatus: newDisplayStatus
		});
	}

	handleChangeMaxResults(value) {
		this.setState({
			maxResults: value
		});
	}

	handleDraggerChange(val) {
		this.setState({
	    	retDisplay: "block",
			retVal: val
		});
	}

	handleChange(value) {
    	this.setState({ targetKeys: value });
  	}

  	handleChangeSelect(value) {
    	this.setState({ selectedKeys: value });
  	}

	handleAnalysis() {
		this.setState({
			spinning: true
		});

		const targetKeys = this.state.targetKeys;
		const retVal = this.state.retVal;
		var selectedFiles = [];
		for (var i = 0; i < targetKeys.length; i++)
		{
			selectedFiles.push(retVal[targetKeys[i]]["name"]);
		}
		var filesStr = selectedFiles.join(",");
		var data = { files: filesStr };
		$.ajax({
			type: "POST", 
			url: adminUrl + "analysis",
			data: data, 
			dataType: "json",
			success: function(data) {
				this.setState({
					analysisResult: data,
					spinning: false
				})
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	handleRefresh() {
		this.setState({
			refreshSpinning: true
		});

		$.ajax({
			type: "GET", 
			url: adminUrl + "refresh?max=" + this.state.refreshMaxResults,
			dataType: "text",
			success: function(data) {
				this.setState({
					refreshSpinning: false
				})
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}
	
	handleChangeRefreshMaxResults(value) {
		this.setState({
			refreshMaxResults: value
		});
	}

	handleClear() {
		this.setState({
			clearSpinning: true
		});

		$.ajax({
			type: "GET", 
			url: adminUrl + "clear",
			dataType: "text",
			success: function(data) {
				this.setState({
					clearSpinning: false
				})
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	handleBeautify() {
		this.setState({
			beautifySpinning: true
		});

		$.ajax({
			type: "GET", 
			url: adminUrl + "beautify",
			dataType: "text",
			success: function(data) {
				message.success('Beautify done');
				this.setState({
					beautifySpinning: false
				})
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	handleSync(data) {
		this.setState({
			syncSpinning: true
		});

		$.ajax({
			type: "POST", 
			url: adminUrl + "sync",
			data: data, 
			dataType: "text",
			success: function() {
				message.success('Sync successfully');
				this.setState({
					syncSpinning: false
				})
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
			<Layout style={{ height: pageHeight }}>
				<Sider breakpoint="lg" collapsedWidth="0" style={{ height: "100%", textAlign: "left" }} width={250}>
					<div className="logo">Haystack Admin</div>
    				<Menu 
    					theme="dark" 
    					defaultSelectedKeys={['4']} 
    					style={{ height: "100%" }}
    					onClick={this.handleClickMenuItem}
    				>
     		 			<Menu.Item key="1" style={{ height: "48px", lineHeight: "48px", fontSize: 13, padding: "0 24px" }}>
        					<Icon type="shopping-cart" style={{ fontSize: 15 }} />
        					<span className="nav-text">Add Product</span>
      					</Menu.Item>
      					<Menu.Item key="2" style={{ height: "48px", lineHeight: "48px", fontSize: 13, padding: "0 24px" }}>
        					<Icon type="cloud-upload-o" style={{ fontSize: 15 }} />
        					<span className="nav-text">Upload Picture</span>
      					</Menu.Item>
				      	<Menu.Item key="3" style={{ height: "48px", lineHeight: "48px", fontSize: 13, padding: "0 24px" }}>
					        <Icon type="line-chart" style={{ fontSize: 15 }} />
					        <span className="nav-text">Analysis</span>
				      	</Menu.Item>
     		 			<Menu.Item key="4" style={{ height: "48px", lineHeight: "48px", fontSize: 13, padding: "0 24px" }}>
        					<Icon type="sync" style={{ fontSize: 15 }} />
        					<span className="nav-text">Refresh</span>
      					</Menu.Item>
     		 			<Menu.Item key="5" style={{ height: "48px", lineHeight: "48px", fontSize: 13, padding: "0 24px" }}>
        					<Icon type="delete" style={{ fontSize: 15 }} />
        					<span className="nav-text">Clear</span>
      					</Menu.Item>
     		 			<Menu.Item key="6" style={{ height: "48px", lineHeight: "48px", fontSize: 13, padding: "0 24px" }}>
        					<Icon type="smile-o" style={{ fontSize: 15 }} />
        					<span className="nav-text">Beautify</span>
      					</Menu.Item>
     		 			<Menu.Item key="7" style={{ height: "48px", lineHeight: "48px", fontSize: 13, padding: "0 24px" }}>
        					<Icon type="download" style={{ fontSize: 15 }} />
        					<span className="nav-text">Sync</span>
      					</Menu.Item>
   					 </Menu>
  				</Sider>
    			<Content style={{ height: "100%", background: "#fff" }}>
    				<AddProductBox 
    					display={this.state.displayStatus[0]}
    				/>
    				<UploadPictureBox
    					display={this.state.displayStatus[1]} 
    					maxResults={this.state.maxResults} 
    					retDisplay={this.state.retDisplay} 
    					retVal={this.state.retVal}
    					handleChangeMaxResults={this.handleChangeMaxResults} 
    					handleDraggerChange={this.handleDraggerChange}
    				/>
    				<div className="analysis-box" style={{ display: this.state.displayStatus[2] }}>
	    				<Spin spinning={this.state.spinning} style={{ position: "absolute", top: 0, left: 0 }}>
		    				<AnalysisBox 
					  			onChangeTransfer={this.handleChange} 
					  			onChangeTransferSelect={this.handleChangeSelect} 
					  			onAnalysis={this.handleAnalysis} 
					  			retVal={this.state.retVal} 
					  			targetKeys={this.state.targetKeys} 
					  			selectedKeys={this.state.selectedKeys} 
					  		/>
				  			<AnalysisResult 
				  				analysisRes={this.state.analysisResult}  
				  			/>
			  			</Spin>
			  		</div>
			  		<div style={{ display: this.state.displayStatus[3], marginTop: "200px" }}>
				  		<Spin spinning={this.state.refreshSpinning} style={{ width: "auto" }}>
				  			<RefreshBox 
    							refreshMaxResults={this.state.refreshMaxResults} 
				  				refreshSpinning={this.state.refreshSpinning} 
				  				onRefresh={this.handleRefresh} 
				  				onChangeRefreshMaxResults={this.handleChangeRefreshMaxResults}
				  			/>
				  		</Spin>
		  			</div>
			  		<div style={{ display: this.state.displayStatus[4], marginTop: "300px" }}>
				  		<Spin spinning={this.state.clearSpinning} style={{ width: "auto" }}>
				  			<ClearBox 
				  				clearSpinning={this.state.clearSpinning} 
				  				onClear={this.handleClear}
				  			/>
				  		</Spin>
		  			</div>
			  		<div style={{ display: this.state.displayStatus[5], marginTop: "300px" }}>
				  		<Spin spinning={this.state.beautifySpinning} style={{ width: "auto" }}>
				  			<BeautifyBox 
				  				beautifySpinning={this.state.beautifySpinning} 
				  				onBeautify={this.handleBeautify}
				  			/>
				  		</Spin>
		  			</div>
			  		<div style={{ display: this.state.displayStatus[6], marginTop: "160px" }}>
				  		<Spin spinning={this.state.syncSpinning} style={{ width: "auto" }}>
				  			<SyncBox 
				  				syncSpinning={this.state.syncSpinning} 
				  				onSync={this.handleSync}
				  			/>
				  		</Spin>
		  			</div>
    			</Content>
  			</Layout>
	  	);
	}
}