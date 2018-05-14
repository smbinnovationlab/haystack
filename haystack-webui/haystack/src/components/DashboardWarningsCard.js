'use strict';

import { Card } from 'antd';
import ReactEcharts from "echarts-for-react";
import echarts from 'echarts/lib/echarts';
import 'echarts/lib/chart/bar';

import "../css/HomePage.css";


export default class DashboardWarningsCard extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const events = this.props.events;
		var warningEvents = new Array();
		for (var i = 0; i < events.length; i++) {
			if (events[i]["product_price_compare"] != "normal") {
				var date = events[i]["event_time"].substr(0, 10);
				if (warningEvents.hasOwnProperty(date))
					warningEvents[date] += 1;
				else
					warningEvents[date] = 1;
			}
		}
		var eventsDate = [], eventsCnt = [];
		for (var e in warningEvents) {
			eventsDate.push(e);
			eventsCnt.push(warningEvents[e]);
		}

		var option = {
			grid: [
                {
                	left: 0,
                	top: 0,
                    width: '100%', 
                    height: '100%' 
                },
            ],
            tooltip : {
		        trigger: 'item',
		        formatter: '{b} : {c} Activities',
		        backgroundColor: '#eaeaea',
		        textStyle: {
		        	fontSize: 12,
					color: '#37474f'
		        }
		    },
			xAxis: {
		        data: eventsDate,
		        show: false
		    },
		    yAxis: {
		    	show: false
		    },
		    dataZoom: [
		        {
		            type: 'inside'
		        }
		    ],
			series: [
		        {
		            type: 'bar',
		            tooltip: {
		                position: 'top'
		            },
		            itemStyle: {
		                normal: {
		                    color: new echarts.graphic.LinearGradient(
		                        0, 0, 0, 1,
		                        [
		                            {offset: 1, color: '#FDDDA0'},
		                            {offset: 0, color: '#FF6C17'}
		                        ]
		                    ),
		                    barBorderRadius: 24
		                },
		                emphasis: {
		                    color: '#FF6C17'
		                },
		            },
	                barWidth: 6,
		            data: eventsCnt
		        }
		    ]
		};

		return (
			<div className="dashboard-card">
				<div className="dashboard-card-title">Alerts</div>
				<div className="dashboard-card-body" style={{ padding: "48px 2px 4px 2px" }}>
					<ReactEcharts 
						option={option} 
						style={{ width: "100%", height: "100%", padding: 0 }} 
					/>
				</div>
			</div>
		);
	}
}