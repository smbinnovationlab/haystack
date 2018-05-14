'use strict';
import { Modal, Button, Tabs, Pagination, message, Icon } from 'antd';
const TabPane = Tabs.TabPane;
import {
  HashRouter as Router,
  Route,
  Link
} from 'react-router-dom';
import ReactEcharts from "echarts-for-react";
import echarts from 'echarts/lib/echarts';
import 'echarts/lib/chart/scatter';

import "../css/PopSiteDetail.css"
import "../css/ModifiedAntd.css"
import "../utils/CurrencySymbolMapper.js"
import "../utils/Conf.js"


export default class PopSiteDetail extends React.Component {
	constructor(props) {
		super(props); 
		this.canclePopSite = this.canclePopSite.bind(this);
		this.addToFavourites = this.addToFavourites.bind(this);
		this.changeHistoryMonth = this.changeHistoryMonth.bind(this);
		this.changeActiveKey = this.changeActiveKey.bind(this);
	}

	changeActiveKey(key) {
		this.props.onChangeActiveKey(key);
	}

    changeHistoryMonth(pageNumber) {
        this.props.onChangeSiteHistoryMonth(pageNumber);
    }

	canclePopSite() {
		this.props.onCanclePopSite();
	}

	addToFavourites() {
		var productId = this.props.popSite["product_id"];
		var data = {
			product_id: productId
		};
		$.ajax({
			type: 'POST',
			url: severUrl + "add_to_favourites",
			data: data,
			dataType: "text",
			success: function() {
				message.success('Added successfully');
			}.bind(this),
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				message.error('Failed to add');
				console.log(XMLHttpRequest.status);
 				console.log(XMLHttpRequest.readyState);
 				console.log(textStatus);
			}.bind(this)
		});
		this.props.onAddToFavourites(productId);
	}

	render() {
		const popSite = this.props.popSite;
		var picUrl = null, priceCompare = null, productCurrency = null;
		if (typeof(popSite) != "undefined") {
			picUrl = "url(/src/pic/screenshot/" + popSite["product_site_id"] + ".png)";

			productCurrency = popSite["currency"];
			if (typeof(currencySymbolMapper[productCurrency]) != "undefined")
				productCurrency = currencySymbolMapper[productCurrency];

			if (popSite['current_price_compare'] == "high") {
				priceCompare = "TOO HIGH";
			} else if (popSite['current_price_compare'] == "low") {
				priceCompare = "TOO LOW";
			} else {
				priceCompare = "";
			}
		}

		var lastIndexed = compareTime(this.props.popSite["last_indexed"]);

		// for chart
		var historyMonth = this.props.siteHistoryMonth;

		var chartData = [];
		var data1 = [];		// normal
		var data2 = [];		// too high or too low
		if (typeof(popSite) != "undefined") {
			var siteEvents = popSite["events"];
			if (typeof(siteEvents) != "undefined") {
				for (var i = 0; i < siteEvents.length; i++) {
					var eventTime = siteEvents[i]["event_time"];
					var eventMonth = parseInt(eventTime.substring(5, 7));
					if (eventMonth == historyMonth) {
						var temp = [];
						temp.push(parseInt(eventTime.substring(8, 10)));
						temp.push(siteEvents[i]["product_price"]);
						if (siteEvents[i]["product_price_compare"] == "normal") {
							data1.push(temp);
						} else {
							data2.push(temp);
						}
					}
				}
			}
		}
		chartData.push(data1);
		chartData.push(data2);

		var chartOption = {
            grid: [
                {
                	left: '5%',
                	top: '15%',
                    width: '90%', 
                    height: '73%' 
                },
            ],
            xAxis: [
                { 
                    gridIndex: 0, 
                    min: 0, 
                    max: 31,
                    splitNumber: 6,
                    splitLine: {show: false},
                    axisLine: {show: false},
                },
            ],
            yAxis: [
                { 
                    gridIndex: 0, 
                    splitLine: {
                        show: true,
                        lineStyle: {type: 'dashed'},
                    },
                    axisLine: {show: false},
                    axisTick: {show: false},
                    axisLabel: {show: false},
                },
            ],
            series: [
                {
                    name: 'normal',
                    data: chartData[0],
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    symbolSize: 13,
                    label: {
			            normal: {
			                show: true,
			                formatter: function (param) {
			                    return productCurrency + parseInt(param.data[1]).toLocaleString();
			                },
			                color: '#9b9b9b',
			                position: 'top'
			            }
			        },
                    itemStyle: {
                    	normal: {color: '#20cec0'}
                    },
                    lineStyle: {
                    	normal: {
                    		color: '#9b9b9b',
                    		width: 2,
                    	}
                    }
                },
                {
                    name: 'abnormal',
                    data: chartData[1],
                    type: 'line',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    symbolSize: 13,
                    label: {
			            normal: {
			                show: true,
			                formatter: function (param) {
			                    return productCurrency + parseInt(param.data[1]).toLocaleString();
			                },
			                color: '#9b9b9b',
			                position: 'top'
			            }
			        },
                    itemStyle: {
                    	normal: {color: '#ff7000'}
                    },
                    lineStyle: {
                    	normal: {
                    		color: '#9b9b9b',
                    		width: 2,
                    	}
                    },
                },
            ],
            backgroundColor: '#ffffff'
        };

		return (
	        <Modal 
	        	wrapClassName="vertical-center-modal"
	        	visible={this.props.popSiteDetailVisible}
	        	onCancel={this.canclePopSite}
	        	footer={null} 
          		width={870} 
	        >
	        	<div className="pop-box">
	        		<div className="pop-image-box" style={{ backgroundImage: picUrl }}></div>
	        		<div className="pop-content">
	        			<div className="pop-text" style={{ marginBottom: "6px" }}>Site: {popSite["domain"]}</div>
	        			<div className="pop-url-box"><a target="_blank" className="pop-url" href={popSite["full_url"]}>{popSite["full_url"]}</a></div>
	        			<div className="pop-name">
	        				{"Product: "}
	        				<Link 
	        					to={"/detail/" + popSite["product_id"] + "/"} 
	        					style={{ color: "#37474f", fontWeight: "bold" }} 
	        				>
	        					{popSite["product_name"]}
	        				</Link>
	        			</div>
	        			<div className="pop-text">
	        				<span className="pop-text">Price:</span>
	        				<span className="pop-price">&nbsp;{productCurrency}{priceFormatter(parseFloat(popSite["current_price"]))}&nbsp;&nbsp;&nbsp;</span>
	        				<span className="pop-price-compare">{priceCompare}</span>
	        			</div>
	        			<Tabs activeKey={this.props.popSiteActiveKey} onChange={this.changeActiveKey} >
							<TabPane tab="Details" key="details" style={{ marginTop: "-16px" }}>
								<div className="pop-info-box">
									<div style={{ marginBottom: "16px" }}>Stauts: {popSite['current_product_status']}</div>
									<div style={{ marginBottom: "16px" }}>Country: {popSite["country"]}</div>
									<div style={{ marginBottom: "16px" }}>Type: {popSite["site_type"]}</div>
									<div>Last Indexed: {lastIndexed}</div>
								</div>
							</TabPane>
							<TabPane tab="Price History" key="price" style={{ marginTop: "-16px" }}>
								<ReactEcharts
				                    option={chartOption}
				                    style={{ height: '192px', width: '100%' }}
				                    className='price-history' 
				                />
				                <div className="pop-chart-pagination">
				                    <Pagination simple current={historyMonth} total={120} onChange={this.changeHistoryMonth} size="small" />
				                </div>
							</TabPane>
						</Tabs>
	        			<Button className="pop-btn" style={{ width: 150 }}>Send email</Button>
	        		</div>
	        	</div>
	        </Modal>
		);
	}
}


function compareTime(inputDate) {
	var nowTime = Date.parse(new Date()) / 1000;
	var inputTime = Date.parse(new Date(inputDate)) / 1000;
	var timeDiff = nowTime - inputTime;
	if (timeDiff < 60 * 60) {
		var minDiff = Math.ceil(timeDiff / 60);
		if (minDiff == 1)
			return minDiff + " min ago";
		else
			return minDiff + " mins ago";
	} else if (timeDiff < 24 * 60 * 60) {
		var hourDiff = Math.ceil(timeDiff / (60 * 60));
		if (hourDiff == 1)
			return hourDiff + " hour ago";
		else
			return hourDiff + " hours ago";
	} else {
		var dayDiff = Math.ceil(timeDiff / (24 * 60 * 60));
		if (dayDiff == 1)
			return dayDiff + " day ago";
		else
			return dayDiff + " days ago";
	}
}