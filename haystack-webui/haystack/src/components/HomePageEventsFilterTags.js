'use strict';

import { Checkbox, Tag } from 'antd';
const CheckableTag = Tag.CheckableTag;

import '../css/HomePage.css';
import '../css/ModifiedAntd.css';


const pageHeight = document.body.clientHeight;


export default class HomePageEventsFilterTags extends React.Component {
	constructor(props) {
		super(props);
		this.changeEventsFilterTags = this.changeEventsFilterTags.bind(this);
	}

	changeEventsFilterTags(id, checked) {
		this.props.onChangeEventsFilterTags(id, checked);
	}

	render() {
		const eventsFilterTags = this.props.eventsFilterTags;
		return (
			<div className="tags-box" style={{ height: (pageHeight - 92) / 2 }}>
				<div className="tags-box-title">Tags filter</div>
				{eventsFilterTags.map((tag) => {
					return (
						<CheckableTag 
							key={tag["id"]} 
							checked={tag["status"]} 
							onChange={checked => this.changeEventsFilterTags(tag["id"], checked)} 
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