'use strict';
import { Checkbox, Tag } from 'antd';
const CheckableTag = Tag.CheckableTag;

import '../css/HomePage.css';
import '../css/ModifiedAntd.css';


const pageHeight = document.body.clientHeight;


export default class HomePageProductsCatergories extends React.Component {
	constructor(props) {
		super(props);
		this.changeProductsCatergories = this.changeProductsCatergories.bind(this);
	}
	
	changeProductsCatergories(id, checked) {
		this.props.onChangeProductsCatergories(id, checked);
	}

	render() {
		const productsCatergories = this.props.productsCatergories;
		return (
			<div className="tags-box" style={{ height: (pageHeight - 92) / 2, borderBottom: 0  }}>
				<div className="tags-box-title">Catergories</div>
				{productsCatergories.map((tag) => {
					return (
						<CheckableTag 
							key={tag["id"]} 
							checked={tag["status"]} 
							onChange={checked => this.changeProductsCatergories(tag["id"], checked)} 
						>
							<span className="tag-text" >{tag["text"]}</span>
						</CheckableTag>
					);
				})}
			</div>
		);
	}
}