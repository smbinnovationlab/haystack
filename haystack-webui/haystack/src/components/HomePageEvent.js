'use strict';
import { Card } from 'antd';
import {
  HashRouter as Router,
  Route,
  Link
} from 'react-router-dom';

import "../css/HomePage.css"
import "../utils/CurrencySymbolMapper.js"
import "../utils/PriceOperation.js"


export default class HomePageEvent extends React.Component {
	constructor(props) {
		super(props);
		this.clickEvent = this.clickEvent.bind(this);
		this.clickDomain = this.clickDomain.bind(this);
		this.loadImgFailed = this.loadImgFailed.bind(this);
	}

	clickEvent() {
		this.props.onClickEvent(this.props.product_site_id, this.props.event_id);
	}

	clickDomain(e) {
		e.stopPropagation();
	}

	loadImgFailed(e) {
		var evtTarget = e.target || e.srcElement;
		document.getElementById("img" + evtTarget.id).style.display = "none";
		document.getElementById("header" + evtTarget.id).style.marginLeft = "8px";
	}

	render() {
		let cardStyle = { 
			width: '100%', 
			height: '160px', 
			textAlign: 'left', 
			borderColor: '#d9d9d9', 
			borderRadius: '8px',
			float: 'left'
		};
		let imageStyle = { 
			float: 'left', 
			marginRight: 8,
			verticalAlgin: 'center' 
		};
		if (this.props.product_price_compare != "normal") {
			cardStyle['borderLeft'] = '8px solid #ff7000';
		} else {
			imageStyle['borderTopLeftRadius'] = '8px';
			imageStyle['borderBottomLeftRadius'] = '8px';
		}

		let timeInfo = compareTime(this.props.event_time);

		let eventType = this.props.event_type;
		let headerText = null, content = null;
		let productCurrency = this.props.currency;
		if (typeof(currencySymbolMapper[productCurrency]) != "undefined")
			productCurrency = currencySymbolMapper[productCurrency];

		if (eventType == "add") {
			headerText = "New Site";
			content = (
				<div className="event-content">
					<a target="_blank" href={this.props.full_url} className="event-domain" onClick={this.clickDomain}>{this.props.domain}</a>
					<span>{' '}has started selling{' '}</span>
					<Link to={"/detail/" + this.props.product_id + "/"}>
						<span className="event-name">{this.props.product_name}</span>
					</Link>
					<span>{' '}and selling at a price of{' '}</span>
					<span>{productCurrency}{priceFormatter(parseFloat(this.props.product_price))}</span>
					<span>{this.props.product_price_compare === "normal" ? "." : " which seems too " + this.props.product_price_compare + "."}</span>
				</div>
			);
		} else if (eventType == "update") {
			headerText = "Price Update";
			content = (
				<div className="event-content">
					<a target="_blank" href={this.props.full_url} className="event-domain" onClick={this.clickDomain}>{this.props.domain}</a>
					<span>{' '}has updated the price of{' '}</span>
					<Link to={"/detail/" + this.props.product_id + "/"}>
						<span className="event-name">{this.props.product_name}</span>
					</Link>
					<span>{' '}to{' '}</span>
					<span>{productCurrency}{priceFormatter(parseFloat(this.props.product_price))}</span>
					<span>{this.props.product_price_compare === "normal" ? "." : " which seems too " + this.props.product_price_compare + "."}</span>
				</div>
			);
		} else {
			headerText = "remove"
			content = (
				<div className="event-content">
					<span className="event-domain">{this.props.domain}</span>
					<span>{' '}has stopped selling{' '}</span>
					<Link to={"/detail/" + this.props.product_id + "/"}>
						<span className="event-name">{this.props.product_name}</span>
					</Link>
				</div>
			);
		}

		var imgUrl = "/src/pic/screenshot/" + this.props.product_site_id + ".png";

		return (
			<div>
				<Card style={cardStyle} bodyStyle={{ padding: 0 }} onClick={this.clickEvent}>
					<div id={"img" + this.props.event_id}>
						<img height={158} src={imgUrl} style={imageStyle} id={this.props.event_id} onError={this.loadImgFailed} />
					</div>
					<span className="event-header" id={"header" + this.props.event_id}>{headerText}</span>
					<span className="event-header event-time">{timeInfo}</span>
					<br/><br/>
					{content}
				</Card>
			</div>
		);
	}
}


function compareTime(inputDate) {
	var nowTime = Date.parse(new Date()) / 1000;
	var inputTime = Date.parse(new Date(inputDate)) / 1000;
	var timeDiff = nowTime - inputTime;
	if (timeDiff < 60 * 60) {
		var minDiff = Math.ceil(timeDiff / 60);
		if (minDiff == 1)
			return minDiff + " min ago";
		else
			return minDiff + " mins ago";
	} else if (timeDiff < 24 * 60 * 60) {
		var hourDiff = Math.ceil(timeDiff / (60 * 60));
		if (hourDiff == 1)
			return hourDiff + " hour ago";
		else
			return hourDiff + " hours ago";
	} else {
		var dayDiff = Math.ceil(timeDiff / (24 * 60 * 60));
		if (dayDiff == 1)
			return dayDiff + " day ago";
		else
			return dayDiff + " days ago";
	}
}