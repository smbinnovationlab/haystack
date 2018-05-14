'use strict';
import { Affix, Layout, Checkbox, Select, Button, Icon, Radio, Table } from 'antd';
const { Sider, Content } = Layout;
const { Column, ColumnGroup } = Table;
const Option = Select.Option;

import '../css/HomePage.css';
import '../css/ModifiedAntd.css';
import HomePageChart from './HomePageChart.js';
import "../utils/CurrencySymbolMapper.js"


const pageWidth = document.body.clientWidth;


class ProductsSorters extends React.Component {
	constructor(props) {
		super(props);
		this.changeProductsSorters = this.changeProductsSorters.bind(this);
	}

	changeProductsSorters(e) {
		this.props.onChangeProductsSorters(e.target.name);
	}

	render() {
		const productsSorters = this.props.productsSorters;
		var iconType = [];
		for (var i = 0; i < productsSorters.length; i++) {
			if (productsSorters[i]["active"])
			{
				if (productsSorters[i]["order"] == "ascend")
					iconType.push("arrow-up");
				else
					iconType.push("arrow-down");
			} else {
				iconType.push("");
			}
		}
		return (
			<div style={{ width: pageWidth - 270 - 51 * 2, float: 'left'}}>
				<Radio.Group>
					<Radio.Button 
						name="productName" 
						value="productName" 
						onClick={this.changeProductsSorters}
					>
						Name <Icon type={iconType[0]} />
					</Radio.Button>
					<Radio.Button 
						name="productPrice" 
						value="productPrice" 
						onClick={this.changeProductsSorters}
					>
						Price <Icon type={iconType[1]} />
					</Radio.Button>
				</Radio.Group>
			</div>
		);
	}
}


class ProductsCategories extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<Select defaultValue="all" onChange={this.handleSelectChange} style={{ width: 120, position: "absolute", right: 22 }}>
				<Option value="all">All Categories</Option>
			</Select>
		);
	}
}


class ProductsTable extends React.Component {
	constructor(props) {
		super(props);
		this.onRowClick = this.onRowClick.bind(this);
	}

	onRowClick(record) {
		window.location = "/#/detail/" + record["productId"] + "/";
	}

	render() {
		const products = this.props.products;
		const productsSorters = this.props.productsSorters;
		const productsFilterTags = this.props.productsFilterTags;

		var selectedTags = [];
		var filteredProducts = [];
		for (var i = 0; i < productsFilterTags.length; i++) {
			if (productsFilterTags[i]['status'] == true)
				selectedTags.push(productsFilterTags[i]);
		}
		if (selectedTags.length > 0) {
			for (var i = 0; i < products.length; i++) {
				var product = products[i];
				for (var j = 0; j < selectedTags.length; j++) {
					var tag = selectedTags[j];
					if (product["price_change"] == tag["id"]) {
						filteredProducts.push(product);
						break;
					}
				}
			}
		} else {
			filteredProducts = products;
		}

		const tableData = [];
		for (var i = 0; i < filteredProducts.length; i++) {
			var priceIndicator = null;
			var productCurrency = filteredProducts[i]["currency"];
			if (typeof(currencySymbolMapper[productCurrency]) != "undefined")
				productCurrency = currencySymbolMapper[productCurrency];

			if (filteredProducts[i]["avg_price_compare"] === "high") {
				priceIndicator = ( <Icon type="arrow-up" className="product-price-increase" />);
			} else if (filteredProducts[i]["avg_price_compare"] === "low") {
				priceIndicator = ( <Icon type="arrow-down" className="product-price-decrease" />);
			}

			var key = filteredProducts[i]["product_id"];
			var productName = filteredProducts[i]["product_name"];
			var productPrice = productCurrency + priceFormatter(parseFloat(filteredProducts[i]["avg_price"])) 
							   + " avg. (" + productCurrency + priceFormatter(parseFloat(filteredProducts[i]["min_price"])) 
							   + "~" + productCurrency + priceFormatter(parseFloat(filteredProducts[i]["max_price"])) + ")";
			var productPicture = "/src/pic/product_main/" + filteredProducts[i]["sku_id"];
			var temp = {
				key: key,
				productId: filteredProducts[i]["product_id"],
				productPicture: productPicture,
				productName: productName,
				productPrice: productPrice,
				avgPrice: filteredProducts[i]["avg_price"],
				priceChange: priceIndicator,
				productStatus: filteredProducts[i]["finished_sites_count"] + " / " + filteredProducts[i]["sites_count"]
			};
			tableData.push(temp);
		}

		const columns = [{
			title: "Product Picture",
			dataIndex: "productPicture",
			key: "productPicture",
			width: 40,
			sortOrder: false,
			render: path => (
				<img src={path} width={40} style={{ margin: "6px 16px 6px 6px" }}/>
			),
		}, {
			title: "Product Name",
			dataIndex: "productName",
			key: "productName",
			sorter: (a, b) => a.productName.localeCompare(b.productName),
			sortOrder: productsSorters[0]["active"] && productsSorters[0]["order"],
			render: text => (
				<div className="product-name">{text}</div>
			),
		}, {
			title: "Product Status",
			dataIndex: "productStatus",
			key: "productStatus",
			render: text => (
					<div className="product-status">[ {text} ]</div>
			),
		}, {
			title: "Product Price",
			dataIndex: "productPrice",
			key: "productPrice",
			sorter: (a, b) => a.avgPrice > b.avgPrice,
			sortOrder: productsSorters[1]["active"] && productsSorters[1]["order"],
			render: text => (
					<div className="product-price">{text}</div>
			),
		}, {
			title: "Price Change",
			dataIndex: "priceChange",
			key: "priceChange",
			render: text => (text),
		}];

		return (
			<Table 
				columns={columns} 
				dataSource={tableData} 
				pagination={false} 
				showHeader={false} 
				className="product-table" 
				onRowClick={this.onRowClick} 
				style={{ border: 0 }}
			>
			</Table>
		);
	}
}


export default class HomePageProductsTab extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<Content style={{ background: '#fff', padding: '8px 51px 8px 45px' }}>
				<ProductsSorters {...this.props} />
				<br/><br/>
				<ProductsTable {...this.props} />
			</Content>
		);
	}
}