'use strict';
import { Row, Col, Button, Table, message, Modal } from 'antd';
const { Column, ColumnGroup } = Table;
const confirm = Modal.confirm;

import "../utils/CurrencySymbolMapper.js"
import "../utils/Conf.js"
import "../utils/PriceOperation.js"


export default class DetailPageInfoBox extends React.Component {
	constructor(props) {
		super(props);
		this.showConfirm = this.showConfirm.bind(this);
		this.addToFavourites = this.addToFavourites.bind(this);
		this.removeFromFavourites = this.removeFromFavourites.bind(this);
	}

	showConfirm() {
		if (this.props.productInfo["is_favourite"] === false) {
			var addToFavourites = this.addToFavourites;
			confirm({
				title: "Add product to dashboard?",
			    okText: "ADD",
			    cancelText: "CANCEL",
			    onOk() {
			    	addToFavourites();
			    },
			    onCancel() {},
			});
		} else {
			var removeFromFavourites = this.removeFromFavourites;
			confirm({
				title: "Remove product from dashboard?",
			    okText: "REMOVE",
			    cancelText: "CANCEL",
			    onOk() {
			    	removeFromFavourites();
			    },
			    onCancel() {},
			});
		}
	}

	addToFavourites() {
		var productId = this.props.productInfo["product_id"];
		var data = {
			product_id: productId
		};
		$.ajax({
			type: 'POST',
			url: severUrl + "add_to_favourites",
			data: data,
			dataType: "text",
			success: function() {
				message.success('Added successfully');
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				message.error('Failed to add');
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	removeFromFavourites() {
		var productId = this.props.productInfo["product_id"];
		var data = {
			product_id: productId
		};
		$.ajax({
			type: 'POST',
			url: severUrl + "remove_from_favourites",
			data: data,
			dataType: "text",
			success: function() {
				message.success('Removed successfully');
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				message.error('Failed to remove');
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
	}

	render() {
		const productInfo = this.props.productInfo;
		var btnContent = null;
		var btnStyle = { 
			height: "48px",
			position: "absolute",
			marginLeft: "32px",
			bottom: "0px",
			lineHeight: "48px",
			borderRadius: "42px",
			borderColor: "#37474f",
			borderWidth: "2px",
			fontSize: "22px",
			color: "#37474f",
			letterSpacing: "0.35px"
		};
		if (productInfo["is_favourite"] === false) {
			btnContent = "Add to favourites";
			btnStyle['width'] = "224px";
		}
		else {
			btnContent = "Remove from favourites";
			btnStyle['width'] = "300px";
		}

		var picUrl = null, productCurrency = null;
		const tableData = [];

		var tbRowBackground = { background: "#f7f8fa" };
		if (typeof(productInfo) != "undefined") {
			picUrl = "/src/pic/product_main/" + productInfo["sku_id"];
			productCurrency = productInfo["currency"];
			if (typeof(currencySymbolMapper[productCurrency]) != "undefined") 
				productCurrency = currencySymbolMapper[productCurrency];
			
			var cnt = 0;
			if (typeof(productInfo["events"]) != "undefined") {
				for (var i = 0; i < productInfo["events"].length; i++)
				{
					var event = productInfo["events"][i];
					if (event["price_change"] === false) continue;


					var envetCurrency = event["currency"];
					if (typeof(currencySymbolMapper[envetCurrency]) != "undefined") 
						envetCurrency = currencySymbolMapper[envetCurrency];

					var key = event["event_id"];
					var rowStyle = {};
					if (event["product_price_compare"] != "normal")
						rowStyle["borderLeft"] = "8px solid #ff7000";
					if (cnt % 2 === 1)
						rowStyle['background'] = "#f7f8fa";

					var row = null;
					if (event["event_type"] == "add") {
						row = (
							<div className="info-tb-row" style={rowStyle}>
								Appeared on <a target="_blank" href={event["full_url"]} className="info-tb-row-url">{event["domain"]}</a>
								{' '}at a price of{' '}{envetCurrency}{priceFormatter(parseFloat(event["product_price"]))}
							</div>
						);
					} else if (event["event_type"] == "update") {
						row = (
							<div className="info-tb-row" style={rowStyle}>
								Update to {envetCurrency}{priceFormatter(parseFloat(event["product_price"]))} on {" "}
								<a target="_blank" href={event["full_url"]} className="info-tb-row-url">{event["domain"]}</a>
							</div>
						);
					} else {
						row = (
							<div className="info-tb-row" style={rowStyle}>
								Remove from <a target="_blank" href={event["full_url"]} className="info-tb-row-url">{event["domain"]}</a>
							</div>
						);
					}
					tableData.push({ key: key, row: row });
					cnt++;
				}
			}
		}

		const columns = [{ title: "Product Event", dataIndex: "row", key: "row" }];

		return (
			<Row gutter={112} style={{ overflow: "hidden" }}>
				<Col xs={{ span: 24 }} sm={{ span: 12 }} style={{ height: 300 }}>
					<div className="info-image-box">
						<img src={picUrl} width={"100%"} className="info-image" />
					</div>
					<div className="info-content-box">
						<div className="info-product-name">{productInfo["product_name"]}</div>
						<div className="info-product-price">
							<span className="info-product-price-emphasize">{productCurrency}{priceFormatter(parseFloat(productInfo["avg_price"]))}</span>
							<span>{"  avg."}</span><br/>
							<span>({productCurrency}{priceFormatter(parseFloat(productInfo["min_price"]))}{"~"}{productCurrency}{priceFormatter(parseFloat(productInfo["max_price"]))})</span>
						</div>
						<Button style={btnStyle} onClick={this.showConfirm}>{btnContent}</Button>
					</div>
				</Col>
				<Col
					xs={{ span: 24 }} 
					md={{ span: 12 }} 
					style={{ height: 300 }}>
					<Table 
						columns={columns} 
						dataSource={tableData} 
						showHeader={false} 
						pagination={{ pageSize: 5 }}
						className="info-tb"
					>
					</Table>
				</Col>	
			</Row>
		);
	}
}