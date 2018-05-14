import '../index.less';
import { Table } from "antd"

import "../utils/Conf.js"


export default class ApiPage extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		const uploadHeaderColumns = [{
			title: "Field",
			dataIndex: "field",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Value",
			dataIndex: "value",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}];
		const uploadHeaderData = [{
			field: "Content-Type",
			value: "application/form-data"
		}];

		const uploadBodyColumns = [{
			title: "Field",
			dataIndex: "field",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Type",
			dataIndex: "type",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Value",
			dataIndex: "value",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}];
		const uploadBodyData = [{
			field: "file",
			type: "File",
			value: "The image to upload"
		}];

		const uploadResponseColumns = [{
			title: "Field",
			dataIndex: "field",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Type",
			dataIndex: "type",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Value",
			dataIndex: "value",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}];
		const uploadResponseData = [{
			field: "id",
			type: "string",
			value: "The UID of the uploaded image"
		}];

		const uploadExampleCodeInPython 
		= ">>> import requests \n" 
		+ ">>> response = requests.post('[request_url]/api/upload', files={'file': open('[file_path]', 'rb')}) \n"
		+ ">>> response = response.json() \n"
		+ "\n"
		+ "{\"id\": \"12345678-1234-5678-1234-567812345678\"}";


		const productUrlParamColumns = [{
			title: "Field",
			dataIndex: "field",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Value",
			dataIndex: "value",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}];
		const productUrlParamData = [{
			field: "id",
			value: "The UID to returned by the \'upload\' api"
		}];

		const productResponseColumns = [{
			title: "Field",
			dataIndex: "field",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Type",
			dataIndex: "type",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Value",
			dataIndex: "value",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}];
		const productResponseData = [{
			field: "status",
			type: "string",
			value: "\"searching\" / \"processing\" / \"completed\""
		}, {
			field: "results",
			type: "array",
			value: "[object(result)]"
		}];

		const productResponseResultColumns = [{
			title: "Field",
			dataIndex: "field",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Type",
			dataIndex: "type",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Value",
			dataIndex: "value",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}];
		const productResponseResultData = [{
			field: "id",
			type: "string",
			value: ""
		}, {
			field: "domain",
			type: "string",
			value: ""
		}, {
			field: "url",
			type: "string",
			value: ""
		}, {
			field: "doc_price",
			type: "object(price)",
			value: "origin price and currency of the product"
		}, {
			field: "target_price",
			type: "object(price)",
			value: "price and currency of the product exchanged into the target currency"
		}, {
			field: "crawl_time",
			type: "string",
			value: ""
		}];

		const productResponsePriceColumns = [{
			title: "Field",
			dataIndex: "field",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Type",
			dataIndex: "type",
			width: "25%",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}, {
			title: "Value",
			dataIndex: "value",
			render: (text) => (<div className="api-table-text">{text}</div>)
		}];
		const productResponsePriceData = [{
			field: "value",
			type: "float",
			value: ""
		}, {
			field: "currency",
			type: "string",
			value: ""
		}];

		const productExampleCodeInPython 
		= ">>> import requests \n" 
		+ ">>> response = requests.get('[request_url]/api/product', params={'id': '[uid]'}) \n"
		+ ">>> response = response.json() \n"
		+ "\n"
		+ "{ \n" 
		+ "    \"status\": \"completed\", \n"
		+ "    \"results\": [ \n"
		+ "        { \n"
		+ "            \"id\": \"1782\", \n"
		+ "            \"domain\": \"the-unit-store.com\", \n"
		+ "            \"url\": \"https://www.the-unit-store.com/products/note-sleeve-wallet-blue-steel-1\", \n"
		+ "            \"doc_price\": { \n"
		+ "                \"value\": 700, \n"
		+ "                \"currency\": \"HKD\" \n"
		+ "            } \n"
		+ "            \"target_price\": { \n"
		+ "                \"value\": 89.48, \n"
		+ "                \"currency\": \"USD\" \n"
		+ "            } \n"
		+ "            \"crawl_time\": \"2018-01-04 03:02:07\", \n"
		+ "        }, \n"
		+ "        ..., \n"
		+ "    ] \n"
		+ "}";


		return (
			<div className="api-page">
				<h1>The Product Haystack API</h1>
				<br/><br/>
				<div>
					<h2>Method: upload</h2>
					<span>Upload image for analysis.</span>
					<h3 className="api-h3">HTTP Request</h3>
					<span>POST <span className="api-highlight-text">{serviceUrl}/api/upload</span></span>
					<h3 className="api-h3">Header</h3>
					<Table 
						columns={uploadHeaderColumns} 
						dataSource={uploadHeaderData} 
						bordered 
						pagination={false} 
					/>
					<h3 className="api-h3">Body</h3>
					<Table 
						columns={uploadBodyColumns} 
						dataSource={uploadBodyData} 
						bordered 
						pagination={false}
					/>
					<h3 className="api-h3">Response {"<JSON>"}</h3>
					<Table 
						columns={uploadResponseColumns} 
						dataSource={uploadResponseData} 
						bordered 
						pagination={false}
					/>
					<h3 className="api-h3">Example Code {"<Python>"}</h3>
					<Highlight className="python">
						{uploadExampleCodeInPython}
					</Highlight>
				</div>
				<br/><br/><br/>
				<div>
					<h2>Method: product</h2>
					<span>Retrieve product information.</span>
					<h3 className="api-h3">HTTP Request</h3>
					<span>GET <span className="api-highlight-text">{serviceUrl}/api/product</span></span>
					<h3 className="api-h3">URL Parameters</h3>
					<Table 
						columns={productUrlParamColumns} 
						dataSource={productUrlParamData} 
						bordered 
						pagination={false}
					/>
					<h3 className="api-h3">Response</h3>
					<Table 
						columns={productResponseColumns} 
						dataSource={productResponseData} 
						bordered 
						pagination={false}
					/>
					<h4 className="api-h4" style={{ fontStyle: "italic" }}>object: result</h4>
					<Table 
						columns={productResponseResultColumns} 
						dataSource={productResponseResultData} 
						bordered 
						pagination={false}
					/>
					<h4 className="api-h4" style={{ fontStyle: "italic" }}>object: price</h4>
					<Table 
						columns={productResponsePriceColumns} 
						dataSource={productResponsePriceData} 
						bordered 
						pagination={false}
					/>
					<h3 className="api-h3">Example Code {"<Python>"}</h3>
					<Highlight className="python">
						{productExampleCodeInPython}
					</Highlight>
				</div>
			</div>
		);
	}
}