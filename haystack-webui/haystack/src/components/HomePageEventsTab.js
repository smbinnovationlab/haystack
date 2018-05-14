'use strict';

import { Affix, Row, Col, Layout, Checkbox } from 'antd';
const { Sider, Content } = Layout
import { Link } from 'react-router-dom'

import HomePageChart from './HomePageChart.js'
import DetailPage from './DetailPage.js'
import HomePageEvent from './HomePageEvent.js'
import PopSiteDetail from './PopSiteDetail.js'


const pageWidth = document.body.clientWidth;


export default class HomePageEventsTab extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const eventsFilterTags = this.props.eventsFilterTags;
		const events = this.props.events;

		var shownEvents = [];
		for (var i = 0; i < events.length; i++) {
			var event = events[i];
			if (event["price_change"] === true)
				shownEvents.push(event);
		}
		var selectedTags = [];
		for (var i = 0; i < eventsFilterTags.length; i++) {
			if (eventsFilterTags[i]['status'] === true)
				selectedTags.push(eventsFilterTags[i]);
		}
		var filteredEvents = [];
		if (selectedTags.length > 0) {
			for (var i = 0; i < shownEvents.length; i++) {
				var event = shownEvents[i];
				for (var j = 0; j < selectedTags.length; j++) {
					var tag = selectedTags[j];
					if (event.event_type == tag['id']) {
						filteredEvents.push(event);
						break;
					}
				}
			}
		} else {
			filteredEvents = shownEvents;
		}

		return (
			<div style={{ width: "100%"}}>
				<Content style={{ width: "100%", background: '#fafafa', padding: '0 23px 32px 23px'}}>
					<Row gutter={16} style={{ width: "100%" }}>
						{filteredEvents.map((event) => {
							return (
								<Col 
									sm={24} md={12} lg={12} 
									style={{ marginTop: '16px' }}
									key={event.event_id} 
								>
									<HomePageEvent 
										key={event.event_id} 
										{...event}
										{...this.props}
									/>
								</Col>
							);
						})}
					</Row>
				</Content>
				<PopSiteDetail {...this.props} />
			</div>
		);
	}
}