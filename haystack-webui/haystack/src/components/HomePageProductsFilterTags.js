'use strict';
import { Checkbox, Tag } from 'antd';
const CheckableTag = Tag.CheckableTag;

import '../css/HomePage.css';
import '../css/ModifiedAntd.css';


const pageHeight = document.body.clientHeight;


export default class HomePageProductsFilterTags extends React.Component {
	constructor(props) {
		super(props);
		this.changeProductsFilterTags = this.changeProductsFilterTags.bind(this);
	}

	changeProductsFilterTags(id, checked) {
		this.props.onChangeProductsFilterTags(id, checked);
	}

	render() {
		const productsFilterTags = this.props.productsFilterTags;
		return (
			<div className="tags-box" style={{ height: (pageHeight - 92) / 2 }}>
				<div className="tags-box-title">Tags filter</div>
				{productsFilterTags.map((tag) => {
					return (
						<CheckableTag 
							key={tag["id"]} 
							checked={tag["status"]} 
							onChange={checked => this.changeProductsFilterTags(tag["id"], checked)} 
						>
							<span className="tag-text" >{tag["text"]}</span>
						</CheckableTag>
					);
				})}
			</div>
		);
	}
}