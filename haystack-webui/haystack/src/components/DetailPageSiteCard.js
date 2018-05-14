'use strict';
import { Card } from 'antd';

import "../utils/CurrencySymbolMapper.js"
import "../utils/PriceOperation.js"


export default class DetailPageSiteCard extends React.Component {
	constructor(props) {
		super(props);
		this.clickSite = this.clickSite.bind(this);
	}

	clickSite() {
		this.props.onClickSite(this.props.productSiteId);
	}

	render() {
		var productCurrency = this.props.productCurrency;
		if (typeof(currencySymbolMapper[productCurrency]) != "undefined")
			productCurrency = currencySymbolMapper[productCurrency];
		var eventCurrency = this.props.eventCurrency;
		// if (typeof(currencySymbolMapper[eventCurrency]) != "undefined")
			// eventCurrency += " " + currencySymbolMapper[eventCurrency];
		
		var picUrl = "/src/pic/screenshot/" + this.props.productSiteId + ".png";
		var warning = null;
		if (this.props.priceCompare != "normal") {
			warning = (<img src="/src/pic/asset/warning.png" style={{ position: "absolute", right: 0, top: 0, zIndex: "999" }} />);
		}

		return (
			<div style={{ width: "100%" }}>
				<Card
					style={{ width: "100%",
							 borderColor: '#d9d9d9', 
							 borderRadius: '10px',  }} 
					bodyStyle={{ padding: 0 }} 
				>
					{warning}
					<img width="100%" 
						 src={picUrl} 
						 style={{ borderTopLeftRadius: "10px", borderTopRightRadius: "10px" }} 
						 onClick={this.clickSite} 
					/>
					<div style={{ padding: "6px 8px" }}>
						<a target="_blank" href={this.props.fullUrl}  
						   style={{ color: "#000", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}
						>
							{this.props.domain}
						</a>
						<div className="site-card-price">
							{productCurrency}{priceFormatter(parseFloat(this.props.exchangedPrice))}
							{" ("}
							{eventCurrency}{" "}{priceFormatter(parseFloat(this.props.productPrice))}
							{")"}
						</div>
					</div>
				</Card>
			</div>
		);
	}
}