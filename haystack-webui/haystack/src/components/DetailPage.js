'use strict';

import '../css/DetailPage.css';
import DetailPageInfoBox from './DetailPageInfoBox.js'
import DetailPageTabs from './DetailPageTabs.js'
import "../utils/Conf.js"


export default class DetailPage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			productInfo: [],
			popSiteDetailVisible: false,
			popSite: [],
		};

		this.handleClickSite = this.handleClickSite.bind(this);
		this.handleChangeSiteHistoryMonth = this.handleChangeSiteHistoryMonth.bind(this);
		this.handleCanclePopSite = this.handleCanclePopSite.bind(this);
		this.handleChangeActiveKey = this.handleChangeActiveKey.bind(this);
	}

	componentDidMount() {
		var productId = this.props.match.params.id;
		var requestUrl = severUrl + "get_product/" + productId;
		$.ajax({
			url: requestUrl,
			async: false,
			type: "get", 
			dataType: "json",
			success: function(data) {
				// var currentMonth = parseInt(data[0]["events"][0]["event_time"].substring(5, 7));
				this.setState({
					productInfo: data[0]
				});
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	handleClickSite(productSiteId) {
		var url = severUrl + "get_product_site/" + productSiteId + "/-1";
		$.ajax({
			url: url,
			async: false,
			type: "get", 
			dataType: "json", 
			success: function(data) {
				var currentMonth = parseInt(data["current_event_time"].substring(5, 7));
				this.setState({
					popSite: data,
					popSiteActiveKey: 'details',	
					popSiteDetailVisible: true,
					siteHistoryMonth: currentMonth
				});
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				// alert("error");
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	handleCanclePopSite() {
		this.setState({
			popSiteDetailVisible: false
		});
	}

	handleChangeActiveKey(key) {
		this.setState({
			popSiteActiveKey: key
		});
	}

	handleChangeSiteHistoryMonth(month) {
		this.setState({
			siteHistoryMonth: month
		});
	}

	render() {
		return (
			<div className="detail-page">
				<DetailPageInfoBox productInfo={this.state.productInfo} />
				<DetailPageTabs 
					productInfo={this.state.productInfo} 
					popSiteDetailVisible={this.state.popSiteDetailVisible} 
					popSiteActiveKey={this.state.popSiteActiveKey} 
					popSite={this.state.popSite} 
					siteHistoryMonth={this.state.siteHistoryMonth} 
					onClickSite={this.handleClickSite} 
					onCanclePopSite={this.handleCanclePopSite}
					onChangeActiveKey={this.handleChangeActiveKey} 
					onChangeSiteHistoryMonth={this.handleChangeSiteHistoryMonth} 
				/>
			</div>
		);
	}
}