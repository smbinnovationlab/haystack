'use strict';
import { Row, Col } from 'antd';

import "../css/HomePage.css";
import DashboardFavouritesItem from './DashboardFavouritesItem.js'


export default class DashboardFavouritesCard extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const products = this.props.products;
		var favouriteProducts = []
		for (var i = 0; i < products.length; i++) {
			if (products[i]["is_favourite"])
				favouriteProducts.push(products[i]);
		}

		return (
			<div className="dashboard-card">
				<div className="dashboard-card-body" 
					 style={{ width: "100%", height: "auto", minHeight: "60px", padding: "16px 16px 0px 16px" }}>
					<Row gutter={16}>
						{favouriteProducts.map((product) => {
							return (
								<Col xs={12} sm={8} md={6} lg={4} xl={4} key={product["product_id"]}>
									<DashboardFavouritesItem key={product["product_id"]} {...product} {...this.props} />
								</Col>
							);
						})}
					</Row>
				</div>
			</div>
		);
	}
}