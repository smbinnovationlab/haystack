'use strict';
import { Row, Col, Progress } from 'antd';

import '../css/DetailPage.css';
import DetailPageSiteCard from './DetailPageSiteCard.js'
import PopSiteDetail from './PopSiteDetail.js'


export default class DetailPageSitesList extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const productEvents = this.props.productInfo["events"];
		const productCurrency = this.props.productInfo["currency"];

		var progressPercent = Math.round(
			this.props.productInfo["finished_sites_count"] / this.props.productInfo["sites_count"] * 100);
		var progressStatus = "active";
		if (this.props.productInfo["finished_sites_count"] === this.props.productInfo["sites_count"])
			progressStatus = "success";

		var sitesData = []
		productEvents.sort(function(a, b) {
			return a["product_site_id"] - b["product_site_id"];
		});
		var i = 0;
		while (i < productEvents.length) {
			var tempArray = [];
			var cProductSiteId = productEvents[i]["product_site_id"];
			while (i < productEvents.length 
				&& productEvents[i]["product_site_id"] == cProductSiteId) {
				tempArray.push(productEvents[i]);
				i++;
			}

			tempArray.sort(function(a, b) {
				a["event_time"].localeCompare(b["event_time"]);
			});
			var latestEvent = tempArray[0];
			var data = {
				"productSiteId": latestEvent["product_site_id"],
				"productPrice": latestEvent["product_price"],
				"exchangedPrice": latestEvent["exchanged_price"],
				"productCurrency": productCurrency,
				"eventCurrency": latestEvent["currency"],
				"domain": latestEvent["domain"],
				"fullUrl": latestEvent["full_url"],
				"priceCompare": latestEvent["product_price_compare"]
			}
			sitesData.push(data);
		}

		return (
			<div className="tab sites-tab">
				<span>Found on <b>{sitesData.length}</b> sites</span>
				<div className="info-product-progress">
					<Progress percent={progressPercent} status={progressStatus} style={{ width: "224px" }} />
				</div>
				<Row gutter={16}>
					{sitesData.map((site) => {
						return (
							<Col
								key={site["productSiteId"]} 
								xs={12} sm={6} lg={4} 
								style={{ marginTop: '16px' }}
							>
								<DetailPageSiteCard key={site["productSiteId"]} {...site} {...this.props} />
							</Col>
						);
					})}
				</Row>
				<PopSiteDetail {...this.props} />
			</div>
		);
	}
}