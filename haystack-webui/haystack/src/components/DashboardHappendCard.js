'use strict';

import { Card } from 'antd';
import ReactEcharts from "echarts-for-react";
import echarts from 'echarts/lib/echarts';
import 'echarts/lib/chart/pie';

import "../css/HomePage.css";


export default class DashboardHappendCard extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const events = this.props.events;
		var allEventsNum = events.length;
		var addEventsNum = 0, updateEventsNum = 0, removeEventsNum = 0;
		for (var i = 0; i < allEventsNum; i++)
		{
			var event = events[i];
			var eventType = event["event_type"];
			if (eventType == "add")
				addEventsNum++;
			else if (eventType == "update")
				updateEventsNum++;
			else if (eventType == "remove")
				removeEventsNum++;
		}

		var data = [
			{value: addEventsNum, name: "New eCommerce site      " + Math.round(addEventsNum / allEventsNum * 100) + "%"},
			{value: updateEventsNum, name: "Price updates                " + Math.round(updateEventsNum / allEventsNum * 100) + "%"},
			{value: removeEventsNum, name: "eCommerce delisting      " + Math.round(removeEventsNum / allEventsNum * 100) + "%"}
		];

		var option = {
		    legend: {
		        orient: 'vertical',
		        left: '50%',
		        top: 'middle',
		        itemWidth: 16,
		        itemHeight: 16,
		        itemGap: 32,
		        formatter: '{name}',
		        selectedMode: false,
		        textStyle: {
		        	fontSize: 16,
		        },
		        data: data
		    },
		    color: ['#00EEB3', '#FF6C17', '#00ABFB'],
			series: [
		        {
		            type: 'pie',
		            center: ['25%', '50%'],
		            radius: ['62%', '75%'],
            		avoidLabelOverlap: false,
		            label: {
		                normal: {
		                    show: true,
		                    formatter: parseInt(allEventsNum).toLocaleString() + "\nActivities",
		                    position: 'center',
		                    color: '#000',
		                    textStyle: {
		                        fontSize: 30
		                    }
		                }
		            },
		            itemStyle: {
		            	normal: {
		            		borderColor: '#fff',
		            		borderWidth: 8,
		            		borderType: 'solid'
		            	}
		            },
		            data: data,
		            silent: true
		        }
		    ]
		};


		return (
			<div className="dashboard-card">
				<div className="dashboard-card-title">Activities</div>
				<div className="dashboard-card-body">
					<ReactEcharts 
						option={option} 
						className="dashboard-happend-chart" 
						style={{ padding: 0 }} 
					/>
				</div>
			</div>
		);
	}
}