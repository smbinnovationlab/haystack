'use strict';
import { Card } from 'antd';

import "../css/HomePage.css";
import "../utils/CurrencySymbolMapper.js"
import "../utils/PriceOperation.js"


export default class DashboardFavouritesItem extends React.Component {
	constructor(props) {
		super(props);
		this.setPadding = this.setPadding.bind(this);
		this.onItemClick = this.onItemClick.bind(this);
	}

	setPadding() {
		var imgObj = document.getElementById('favourite-item-image-' + this.props.product_id);
		var imgBoxObj = document.getElementById('favourite-item-image-box-' + this.props.product_id);
		
		var imgWidth = imgObj.width;
		var imgHeight = imgObj.height;

		imgBoxObj.style.height = imgWidth + 'px';
		if (imgHeight < imgWidth) {
			var padding = (imgWidth - imgHeight) / 2 + 'px';
			imgBoxObj.style.paddingTop = padding;
			imgBoxObj.style.paddingBottom = padding;

			imgObj.style.borderTopLeftRadius = '0px';
			imgObj.style.borderTopRightRadius = '0px';
		}
	}

	onItemClick() {
		window.location = "/#/detail/" + this.props.product_id + "/";
	}

	render() {
		var productId = this.props.product_id;
		var productPicture = "/src/pic/product_main/" + this.props.sku_id;
		var productCurrency = this.props.currency;
		if (typeof(currencySymbolMapper[productCurrency]) != "undefined")
			productCurrency = currencySymbolMapper[productCurrency];

		var priceIndicator = null;
		var priceCompare = this.props.avg_price_compare;
		if (priceCompare === "high") {
			priceIndicator = (<img src="/src/pic/asset/IC-long-arrow-up.png" style={{ width: "100%" }} />);
		} else if (priceCompare === "low") {
			priceIndicator = (<img src="/src/pic/asset/IC-long-arrow-down.png" style={{ width: "100%" }} />);
		}
		return (
			<Card 
				id="favourite-item-box"
				bodyStyle={{ padding: 0 }} 
				className="favourite-item-box" 
				style={{ borderRadius: "10px", 
						 backgroundColor: "#F5F4F4", 
						 border: "1px solid #F5F4F4", 
						 marginBottom: 16 }} 
				onClick={this.onItemClick}
			>
				<div id={"favourite-item-image-box-" + productId} className="favourite-item-image-box">
					<img src={productPicture} 
						 className="favourite-item-image" 
						 id={"favourite-item-image-" + productId}
						 onLoad={this.setPadding} 
					/>
				</div>
				<div className="favourite-item-content">
					<div className="favourite-item-text">
						<div className="favourite-item-name">{this.props.product_name}</div>
						<div className="favourite-item-price">
							{productCurrency}{priceFormatter(parseFloat(this.props.avg_price))}
							{" ("}
							{productCurrency}{priceFormatter(parseFloat(this.props.min_price))}
							{"~"}
							{productCurrency}{priceFormatter(parseFloat(this.props.max_price))}
							{")"}
						</div>
					</div>
					<div className="favourite-item-arrow">{priceIndicator}</div>
				</div>
			</Card>
		);
	}
}