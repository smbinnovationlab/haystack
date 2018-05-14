'use strict';

import { Checkbox, Tag } from 'antd';
const CheckableTag = Tag.CheckableTag;

import '../css/HomePage.css';
import '../css/ModifiedAntd.css';


const pageHeight = document.body.clientHeight;


export default class HomePageEventsSortTags extends React.Component {
	constructor(props) {
		super(props);
		this.changeEventsSortTags = this.changeEventsSortTags.bind(this);
	}

	changeEventsSortTags(id, checked) {
		this.props.onChangeEventsSortTags(id, checked);
	}

	render() {
		const eventsSortTags = this.props.eventsSortTags;
		return (
			<div className="tags-box" style={{ height: (pageHeight - 92) / 2, borderBottom: 0 }}>
				<div className="tags-box-title">Sort by</div>
				{eventsSortTags.map((tag) => {
					return (
						<CheckableTag 
							key={tag["id"]} 
							checked={tag["status"]} 
							onChange={checked => this.changeEventsSortTags(tag["id"], checked)} 
							style={{ marginTop: "28px" }}
						>
							<span className="tag-text" >{tag["text"]}</span>
						</CheckableTag>
					);
				})}
			</div>
		);
	}
}