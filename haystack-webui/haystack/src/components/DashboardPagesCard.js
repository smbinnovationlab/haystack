'use strict';

import { Card } from 'antd';
import ReactEcharts from "echarts-for-react";
import echarts from 'echarts/lib/echarts';
import 'echarts/lib/chart/line';

import "../css/HomePage.css";


export default class DashboardPagesCard extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const crawledSites = this.props.crawledSites;
		var allSitesNum = crawledSites.length;

		var d = new Date();
		var currentTimestamp = d.getTime();
		var startTimestamp = currentTimestamp - 5 * 60 * 60 * 1000;
		var startD = new Date(startTimestamp);
		var startYear = startD.getFullYear();
		var startMonth = startD.getMonth() + 1;
		var startDate = startD.getDate();
		var startHour = startD.getHours();
		if (startMonth < 10)
			startMonth = "0" + startMonth;
		if (startDate < 10)
			startDate = "0" + startDate;
		if (startHour < 10)
			startHour = "0" + startHour;
		var startDatetime = startYear + "-" + startMonth + "-" + startDate
						   + " " + startHour + ":00:00";
		startD = new Date(startDatetime);

		var lastCrawledSitesNum = 0;
		var restCrawledSites = [];
		for (var i = 0; i < crawledSites.length; i++) {
			var tempD = new Date(crawledSites[i]["last_indexed"]);
			if (tempD < startD)
				lastCrawledSitesNum++;
			else {
				restCrawledSites.push(crawledSites[i]);
			}
		}

		var startTime = startHour + ":00" ;
		var timeData = [startTime];
		var sitesNumData = [lastCrawledSitesNum];
		var n = lastCrawledSitesNum;
		var cIdx = 0;
		for (var i = 1; i < 6 * 60; i++) {
			var tempNum = n;
			var tempD1 = new Date(startD.getTime() + i * 60 * 1000);
			if (tempD1 > d) break;
			var tempSites = [];
			for (var j = 0; j < restCrawledSites.length; j++) {
				var tempD2 = new Date(restCrawledSites[j]["last_indexed"]);
				if (tempD2 < tempD1) {
					tempNum++;
				} else {
					tempSites.push(restCrawledSites[j]);
				}
			}
			var h = tempD1.getHours();
			if (h < 10)
				h = "0" + h;
			var m = i % 60;
			if (m < 10)
				m = "0" + m;
			timeData.push(h + ":" + m);
			sitesNumData.push(tempNum);
			n = tempNum;
			restCrawledSites = tempSites.slice(0);
		}

		var option = {
			grid: [
                {
                	left: 0,
                	top: '10%',
                    width: '100%', 
                    height: '90%' 
                },
            ],
            tooltip: {
        		trigger: 'axis',
        		position: function (pt) {
        			return [pt[0], '10%'];
        		},
        		textStyle: {
        			fontSize: 12,
        		}
    		},
			xAxis: {
				show: true,
		        type: 'category',
		        data: timeData,
		        min: 'dataMin',
		        max: 'dataMax',
		        axisTick: {
		        	inside: true,
		        	interval: 59
		        },
		        axisLabel: {
		        	inside: true,
		        	interval: 59,
		        	align: 'left',
		        	fontSize: 10,
		        	width: '100%'
		        },
		    },
		    yAxis: {
				show: false,
		        type: 'value',
		        min: 0,
		        max: 'dataMax'
		    },
		    series: [
		    	{
		    		type: 'line',
		    		data: sitesNumData,
		            smooth:true,
		            symbol: 'none',
		            itemStyle: {
		            	normal: {
		            		color: '#29F0BE'
		            	}
		            },
		    		lineStyle: {
		    			normal: {
		    				width: 2,
		    				color: new echarts.graphic.LinearGradient(
		    					0, 0, 1, 0, 
		    					[{
                        			offset: 0,
                        			color: '#21F0BC'
                    			}, {
                        			offset: 1,
                        			color: '#23B5FB'
                    			}]
                    		)
		    			}
		    		},
		    		areaStyle: {
		    			normal: {
		    				color: 'rgba(41, 240, 190, 0.05)'
		    			}
		    		}
		    	}
		    ]
		}

		return (
			<div className="dashboard-card" style={{ marginBottom: "8px" }}>
				<div className="dashboard-card-title">Pages</div>
				<div className="dashboard-card-body" style={{ height: "112px", padding: 0 }} >
					<div className="dashboard-pages-text-large">{allSitesNum}</div>
					<div className="dashboard-pages-text-small">pages crawled</div>
					<ReactEcharts 
						option={option} 
						style={{ width: "100%", height: "74px", padding: 0 }} 
					/>
				</div>
			</div>
		);
	}
}