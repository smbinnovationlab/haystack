'use strict';
import { Pagination } from 'antd';
import ReactEcharts from "echarts-for-react";
import echarts from 'echarts/lib/echarts';
import 'echarts/lib/chart/scatter';

import '../css/DetailPage.css';
import "../utils/PriceOperation.js"


export default class DetailPagePriceChart extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		var productInfo = this.props.productInfo;
        var productCurrency = null;

        var date = [];
		var data1 = [], data2 = [];
        var urlData1 = [], urlData2 = [];
        var domainData1 = [], domainData2 = [];
		if (typeof(productInfo) != "undefined") {
            productCurrency = productInfo["currency"];
            if (typeof(currencySymbolMapper[productCurrency]) != "undefined")
                productCurrency = currencySymbolMapper[productCurrency];

			var productEvents = productInfo["events"];
			if (typeof(productEvents) != "undefined") {
				for (var i = 0; i < productEvents.length; i++) {
                    if (productEvents[i]["price_change"] === false)
                        continue;
					var eventTime = productEvents[i]["event_time"].substring(0, 10);
                    if (date.indexOf(eventTime) == -1)
                        date.push(eventTime);
					var temp = [];
                    temp.push(eventTime)
					temp.push(productEvents[i]["exchanged_price"]);
					if (productEvents[i]["product_price_compare"] == "normal") {
						data1.push(temp);
                        urlData1.push(productEvents[i]["full_url"]);
                        domainData1.push(productEvents[i]["domain"]);
					} else {
						data2.push(temp);
                        urlData2.push(productEvents[i]["full_url"]);
                        domainData2.push(productEvents[i]["domain"]);
					}
				}
			}
		}
        
        var urlData = {
            normal: urlData1,
            abnormal: urlData2
        };
        var domainData = {
            normal: domainData1,
            abnormal: domainData2
        }

		var chartOption = {
            grid: [
                {
                	left: '8%',
                	top: '12%',
                    width: '84%', 
                    height: '70%' 
                },
            ],
            tooltip: {
                show: true,
                trigger: 'item',
                enterable: true,
                position: function (pos, params, dom, rect, size) {
                    var obj = {top: pos[1] - size.contentSize[1] / 2};
                    if (pos[0] < size.viewSize[0] / 2) {
                        obj['left'] = pos[0] + 20;
                    } else {
                        obj['left'] = pos[0] - size.contentSize[0] - 20;
                    }
                    return obj;
                },
                formatter: function(params, ticket, callback) {
                    var data = params.data;
                    var url = urlData[params.seriesName][params.dataIndex];
                    var domain = domainData[params.seriesName][params.dataIndex];
                    return data[0] + "<br/><b>" + productCurrency + priceFormatter(parseFloat(data[1])) + "</b>, " 
                           + "<a target=\"_blank\" href=\"" + url + "\">" + domain + "</a>";
                },
                backgroundColor: '#fff',
                borderWidth: 2,
            },
            xAxis: [
                {
                    min: 'dataMin',
                    max: 'dataMax',
                    splitLine: {show: false},
                    axisLine: {show: false},
                    data: date.sort()
                },
            ],
            yAxis: [
                { 
                    splitLine: {
                        show: true,
                        lineStyle: {type: 'dashed'},
                    },
                    axisLine: {show: false},
                },
            ],
            dataZoom: [
                {
                    type: 'slider',
                    show: true,
                    labelPrecision: 0,
                    start: 0,
                    end: 100,
                    top: '88%',
                    handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                    handleSize: '80%',
                    handleStyle: {
                        color: '#fff',
                        shadowBlur: 3,
                        shadowColor: 'rgba(0, 0, 0, 0.6)',
                        shadowOffsetX: 2,
                        shadowOffsetY: 2
                    }
                },
            ],
            series: [
                {
                    name: 'normal',
                    data: data1,
                    type: 'scatter',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    symbol: 'circle',
                    symbolSize: 16,
                    itemStyle: {
                    	normal: {color: '#20cec0'},
                    },
                    hoverAnimation: false,
                    tooltip: {
                        borderColor: '#20cec0',
                        textStyle: {
                            color: '#000',
                            fontSize: 13,
                        },
                    },
                },
                // {
                //     name: 'normal',
                //     data: data1,
                //     type: 'scatter',
                //     xAxisIndex: 0,
                //     yAxisIndex: 0,
                //     symbol: 'circle',
                //     symbolSize: 11,
                //     itemStyle: {
                //         normal: {color: '#fff', opacity: 1},
                //         emphasis: {color: '#20cec0'},
                //     },
                //     hoverAnimation: false,
                //     tooltip: {
                //         borderColor: '#20cec0',
                //         textStyle: {
                //             color: '#000',
                //             fontSize: 13,
                //         },
                //     },
                // },
                {
                    name: 'abnormal',
                    data: data2,
                    type: 'scatter',
                    xAxisIndex: 0,
                    yAxisIndex: 0,
                    symbolSize: 16,
                    itemStyle: {
                    	normal: {color: '#ff7000'}
                    },
                    hoverAnimation: false,
                    tooltip: {
                        borderColor: '#ff7000',
                        textStyle: {
                            color: '#000',
                            fontSize: 13,
                        },
                    },
                }
            ]
        };

		return (
			<div className="tab">
                <ReactEcharts
                    option={chartOption}
                    style={{ height: '560px', width: '100%' }}
                    className='price-history' 
                />
			</div>
		);
	}
}