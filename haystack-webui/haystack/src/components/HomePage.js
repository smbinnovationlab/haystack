'use strict';
import '../index.less';
import { Layout, Row, Col, message } from 'antd';
const { Header, Content, Sider } = Layout;

import HomePageHeader from './HomePageHeader.js'
import HomePageTabs from './HomePageTabs.js'
import "../utils/Conf.js"

export default class HomePage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			popSyncBoxVisible: false,
			popSyncSpinning: false,
			// for Anywhere
			// anywhereServerUrl: "il.anwdmz2.com",
			// anywhereLoginUsername: "test1@sap.com",
			// for B1
			anywhereServerUrl: "INNO_TC",
			anywhereLoginUsername: "manager",
			anywhereLoginPassword: "",
			popSettingBoxVisible: false,
			maxSyncResults: 10,
			crawledSites: [],
			crawledSitesSpinning: true,
			eventsSpinning: true,
			eventsFilterTags: [
				{ id: "add", status: false, text: "New eCommerce site" },
				{ id: "update", status: false, text: "Price updates" },
				{ id: "remove", status: false, text: "eCommerce delisting" }
			],
			eventsSortTags: [
				{ id: "time", status: true, text: "Time" },
				{ id: "priority", status: false, text: "Priority" }
			],
			events: [],
			productsSpinning: true,
			productsFilterTags: [
				{ id: "alert", status: false, text: "Alert" },
				{ id: "increase", status: false, text: "Price increase" },
				{ id: "decrease", status: false, text: "Price decrease" }
			],
			productsCatergories: [
				{ id: "all", status: true, text: "All" }
			],
			productsSorters: [
				{ id: "productName", active: false, order: "ascend" },
				{ id: "productPrice", active: false, order: "ascend" }
			],
			products: [],
			popSiteDetailVisible: false,
			popSite: []
		};

		this.initData = this.initData.bind(this);
		this.handleChangeEventsFilterTags = this.handleChangeEventsFilterTags.bind(this);
		this.handleChangeEventsSortTags = this.handleChangeEventsSortTags.bind(this);
		this.handleMountEventsTab = this.handleMountEventsTab.bind(this);
		this.handleChangeProductsFilterTags = this.handleChangeProductsFilterTags.bind(this);
		this.handleChangeProductsCatergories = this.handleChangeProductsCatergories.bind(this);
		this.handleChangeProductsSorters = this.handleChangeProductsSorters.bind(this);
		this.handleMountProductsTab = this.handleMountProductsTab.bind(this);
		this.handleClickEvent = this.handleClickEvent.bind(this);
		this.handleCanclePopSite = this.handleCanclePopSite.bind(this);
		this.handleChangeSiteHistoryMonth = this.handleChangeSiteHistoryMonth.bind(this);
		this.handleChangeActiveKey = this.handleChangeActiveKey.bind(this);
		this.handleAddToFavourites = this.handleAddToFavourites.bind(this);
		this.handleShowPopSyncBox = this.handleShowPopSyncBox.bind(this);
		this.handleHidePopSyncBox = this.handleHidePopSyncBox.bind(this);
		this.handleChangeSyncInfo = this.handleChangeSyncInfo.bind(this);
		this.handleSync = this.handleSync.bind(this)
		this.handleShowPopSettingBox = this.handleShowPopSettingBox.bind(this);
		this.handleHidePopSettingBox = this.handleHidePopSettingBox.bind(this);
		this.handleChangeMaxSyncResults = this.handleChangeMaxSyncResults.bind(this);
	}

	componentDidMount() {
		var events = null, products = null, crawledSites = null;
		var initData = this.initData;
		// method 1
		$.when(
			$.ajax({
				url: severUrl + "get_events",
				type: "get", 
				dataType: "json"
			}),
			$.ajax({
				url: severUrl + "get_products",
				type: "get", 
				dataType: "json"
			}),
			$.ajax({
				url: severUrl + "get_crawled_sites",
				type: "get", 
				dataType: "json"
			}),
		).done(function(data1, data2, data3) {
			if (data1[1] === "success")
				events = data1[0];
			if (data2[1] === "success")
				products = data2[0];
			if (data3[1] === "success")
				crawledSites = data3[0];
			initData(events, products, crawledSites);
		});
		// method 2
		// var promise1 = $.ajax({
		// 	url: severUrl + "get_events", 
		// 	type: "get", 
		// 	dataType: "json"
		// });
		// var promise2 = promise1.then(function(data) {
		// 	events = data;
		// 	return $.ajax({
		// 		url: severUrl + "get_products",
		// 		type: "get", 
		// 		dataType: "json"
		// 	});
		// });
		// var promise3 = promise2.then(function(data) {
		// 	products = data;
		// 	return $.ajax({
		// 		url: severUrl + "get_crawled_sites",
		// 		type: "get", 
		// 		dataType: "json"
		// 	});
		// });
		// promise3.done(function(data) {  
		// 	crawledSites = data;
		// 	initData(events, products, crawledSites);
		// });
	}

	initData(events, products, crawledSites) {
		this.setState({
			events: events,
			products: products,
			crawledSites: crawledSites,
			eventsSpinning: false,
			productsSpinning: false,
			crawledSitesSpinning: false
		});
		this.forceUpdate();
	}

	handleChangeEventsFilterTags(id, checked) {
		var newTags = this.state.eventsFilterTags;
		for (var i = 0; i < newTags.length; i++)
		{
			if (newTags[i]['id'] == id)
				newTags[i]['status'] = checked;
		}

		this.setState({
			eventsFilterTags: newTags
		});
	}

	handleChangeEventsSortTags(id, checked) {
		var newTags = this.state.eventsSortTags;
		for (var i = 0; i < newTags.length; i++)
		{
			if (newTags[i]['id'] == id)
				newTags[i]['status'] = checked;
		}
		this.setState({
			eventsSortTags: newTags
		});
	}

	handleMountEventsTab(data) {
		this.setState({
			events: data
		});
	}

	handleChangeProductsFilterTags(id, checked) {
		var newTags = this.state.productsFilterTags;
		for (var i = 0; i < newTags.length; i++)
		{
			if (newTags[i]['id'] == id)
				newTags[i]['status'] = checked;
		}
		this.setState({
			productsFilterTags: newTags
		});
	}

	handleChangeProductsCatergories(id, checked) {
		var newTags = this.state.productsCatergories;
		for (var i = 0; i < newTags.length; i++)
		{
			if (newTags[i]['id'] == id)
				newTags[i]['status'] = checked;
		}
		this.setState({
			productsCatergories: newTags
		});
	}

	handleChangeProductsSorters(id) {
		var sorters = this.state.productsSorters;
		for (var i = 0; i < sorters.length; i++) {
			if (sorters[i]['id'] == id) {
				if (sorters[i]['active']) {
					if (sorters[i]['order'] == "ascend")
						sorters[i]['order'] = "descend";
					else if (sorters[i]['order'] == "descend")
						sorters[i]['order'] = "ascend";
				} else sorters[i]['active'] = true;
			} else {
				sorters[i]['active'] = false;
				sorters[i]['order'] = "ascend";
			}
		}
		this.setState({
			productsSorters: sorters
		});
	}

	handleMountProductsTab(data) {
		this.setState({
			products: data
		});
	}

	handleClickEvent(productSiteId, eventId) {
		$.ajax({
			url: severUrl + "get_product_site/" + productSiteId + "/" + eventId,
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

	handleAddToFavourites(productId) {
		var newProducts = this.state.products;
		for (var i = 0; i < newProducts.length; i++)
			if (newProducts[i]["product_id"] == productId)
				newProducts[i]["is_favourite"] = 1;
		this.setState({
			poducts: newProducts
		});
	}

	handleShowPopSyncBox() {
		this.setState({
			popSyncBoxVisible: true
		});
	}

	handleHidePopSyncBox() {
		this.setState({
			popSyncBoxVisible: false
		});
	}

	handleChangeSyncInfo(id, value) {
		if (id === "server") {
			this.setState({
				anywhereServerUrl: value
			});
		} else if (id === "username") {
			this.setState({
				anywhereLoginUsername: value
			});
		} else if (id === "password") {
			this.setState({
				anywhereLoginPassword: value
			});
		}
	}

	handleSync() {
		this.setState({
			popSyncSpinning: true
		});
		var data = {
			server_url: this.state.anywhereServerUrl,
			login_username: this.state.anywhereLoginUsername,
			login_password: this.state.anywhereLoginPassword
		}
		$.ajax({
			type: 'POST',
			// for Anywhere
			// url: severUrl + "sync_from_anywhere?max=" + this.state.maxSyncResults,
			// for B1
			url: severUrl + "sync_from_b1?max=" + this.state.maxSyncResults,
			data: data,
			dataType: "text",
			success: function(data) {
				message.success('Sync successfully');
				this.setState({
					popSyncSpinning: false,
					popSyncBoxVisible: false
				});
				window.location.reload();
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				message.error('Failed to sync');
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}
	
	handleShowPopSettingBox() {
		this.setState({
			popSettingBoxVisible: true
		});
	}

	handleHidePopSettingBox() {
		this.setState({
			popSettingBoxVisible: false
		});
	}

	handleChangeMaxSyncResults(value) {
		this.setState({
			maxSyncResults: value
		});
	}

	render() {
		return (
			<Layout>
				<Header 
					className="home-header" 
					style={{ height: '56px', padding: 0, background: '#fff' }}>
					<HomePageHeader 
						popSyncBoxVisible={this.state.popSyncBoxVisible} 
						popSyncSpinning={this.state.popSyncSpinning} 
						anywhereServerUrl={this.state.anywhereServerUrl} 
						anywhereLoginUsername={this.state.anywhereLoginUsername} 
						anywhereLoginPassword={this.state.anywhereLoginPassword} 
						maxSyncResults={this.state.maxSyncResults} 
						showPopSyncBox={this.handleShowPopSyncBox} 
						hidePopSyncBox={this.handleHidePopSyncBox} 
						onChangeInput={this.handleChangeSyncInfo} 
						onSync={this.handleSync} 
						popSettingBoxVisible={this.state.popSettingBoxVisible} 
						showPopSettingBox={this.handleShowPopSettingBox} 
						hidePopSettingBox={this.handleHidePopSettingBox} 
						onChangeMaxSyncResults={this.handleChangeMaxSyncResults}
					/>
				</Header>
				<Content
					style={{ padding: 0, background: '#fff' }}>
					<HomePageTabs 
						crawledSites={this.state.crawledSites} 
						crawledSitesSpinning={this.state.crawledSitesSpinning} 
						events={this.state.events} 
						eventsFilterTags={this.state.eventsFilterTags} 
						eventsSortTags={this.state.eventsSortTags} 
						eventsSpinning={this.state.eventsSpinning} 
						onChangeEventsFilterTags={this.handleChangeEventsFilterTags} 
						onChangeEventsSortTags={this.handleChangeEventsSortTags} 
						onMountEventsTab={this.handleMountEventsTab} 
						products={this.state.products} 
						productsFilterTags={this.state.productsFilterTags} 
						productsCatergories={this.state.productsCatergories} 
						productsSpinning={this.state.productsSpinning} 
						productsSorters={this.state.productsSorters} 
						onChangeProductsFilterTags={this.handleChangeProductsFilterTags} 
						onChangeProductsCatergories={this.handleChangeProductsCatergories} 
						onChangeProductsSorters={this.handleChangeProductsSorters} 
						onMountProductsTab={this.handleMountProductsTab} 
						popSiteDetailVisible={this.state.popSiteDetailVisible} 
						popSiteActiveKey={this.state.popSiteActiveKey} 
						popSite={this.state.popSite} 
						onClickEvent={this.handleClickEvent} 
						onCanclePopSite={this.handleCanclePopSite}
						siteHistoryMonth={this.state.siteHistoryMonth} 
						onChangeSiteHistoryMonth={this.handleChangeSiteHistoryMonth} 
						onChangeActiveKey={this.handleChangeActiveKey} 
						onAddToFavourites={this.handleAddToFavourites}
					/>
				</Content>
			</Layout>
		);
	}
}