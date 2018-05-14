import { Col, Card, Table } from 'antd';
const { Column, ColumnGroup } = Table;

import "../../utils/Conf.js"


class ResultCard extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const fileName = this.props.product;
		const results = this.props.result;
		var urlsCount = results.length;
		var microdataCount = 0;
		var urlPatternCount = 0;
		var tagPatternCount = 0;
		var errorCount = 0;
		var tableData = [];
		var j = 0;
		for (var i = 0; i < results.length; i++)
		{
			var url = results[i]["url"];
			var status = results[i]["status"];
			var rule = results[i]["rule"];
			var selector = null;
			var weight = null;
			if (typeof(rule) != "undefined")
			{
				selector = rule["selector"];
				weight = rule["weight"];
			}
			var price = results[i]["price"];
			var currency = results[i]["currency"];
			price = currency + " " + price;
			if (status == "microdata" || status == "url pattern") {
				var temp = {
					key: j,
					url: url,
					status: status,
					rule: selector,
					weight: weight,
					price: price
				};
				j++;
				tableData.push(temp);
			}
			else if (status == "tag pattern") {
				var allFound = results[i]["all"];
				for (var k = 0; k < allFound.length; k++) {
					var temp = {
						key: j,
						url: url,
						status: status,
						rule: allFound[k]["rule"]["selector"],
						weight: allFound[k]["rule"]["weight"],
						price: allFound[k]["currency"] + " " + allFound[k]["price"]
					};
					j++;
					tableData.push(temp);
				}
			}

			if (status == "microdata")
				microdataCount++;
			else if (status == "url pattern")
				urlPatternCount++;
			else if (status == "tag pattern")
				tagPatternCount++;
			else if (status == "not found")
				notFoundCount++;
			else if (status == "error")
				errorCount++;
		}
		var foundCount = microdataCount + urlPatternCount + tagPatternCount;
		var notFoundCount = urlsCount - errorCount - foundCount;

		const columns = [{
			title: "url",
			dataIndex: "url",
			key: "url",
			sortOrder: false,
			render: url => (
				<a href={url}>{url}</a>
			),
		}, {
			title: "status",
			dataIndex: "status",
			key: "status",
			width: 100,
			render: text => (
				<p>{text}</p>
			),
		}, {
			title: "rule",
			dataIndex: "rule",
			key: "rule",
			width: 200,
			render: text => (
				<p>{text}</p>
			),
		}, {
			title: "weight",
			dataIndex: "weight",
			key: "weight",
			width: 100,
			render: text => (
				<p>{text}</p>
			),
		}, {
			title: "price",
			dataIndex: "price",
			key: "price",
			width: 120,
			render: text => (
				<p>{text}</p>
			),
		}];


		return (
			<Card title={fileName} style={{ width: "100%" }} style={{ display: this.props.display}}>
				<p><b>All URLs: {foundCount + notFoundCount}</b></p>
				<p><b>Error: {errorCount}</b></p>
				<p><b>Price Not Found: {notFoundCount - errorCount}</b></p>
				<p><b>Price Found: {foundCount}</b></p>
				<p>Mircodata: {microdataCount}</p>
				<p>URL Pattern: {urlPatternCount}</p>
				<p>Tag Pattern: {tagPatternCount}</p>
				<br /><br />
				<Table 
					columns={columns} 
					dataSource={tableData} 
					pagination={true} 
					total={tableData.length}
					pageSize={5}
					size="middle"
				>
				</Table>
			</Card>
		);
	}
}

export default class AnalysisResult extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		var analysisRes = this.props.analysisRes;
		for (var i = 0; i < analysisRes.length; i++)
		{
			analysisRes[i]['id'] = i;
		}

	    return (
	    	<div style={{ width: "100%" }}>
		    	{analysisRes.map((res) => {
		    		return (
		    			<div style={{ width: "100%", background: '#ECECEC', padding: 36 }} key={res["id"]}>
		    				<ResultCard key={res["id"]} {...res} {...this.props} />
		    			</div>
		    		);
		    	})}
	      	</div>
    	);
	}
}