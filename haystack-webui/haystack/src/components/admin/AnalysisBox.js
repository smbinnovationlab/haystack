import { Button, Transfer } from 'antd';

import "../../utils/Conf.js"


export default class AnalysisBox extends React.Component {
	constructor(props) {
		super(props);
		this.doChange = this.doChange.bind(this);
		this.doChangeSelect = this.doChangeSelect.bind(this);
		this.doAnalysis = this.doAnalysis.bind(this);
	}

	doChange(nextTargetKeys) {
    	this.props.onChangeTransfer(nextTargetKeys);
  	}

  	doChangeSelect(sourceSelectedKeys, targetSelectedKeys) {
    	this.props.onChangeTransferSelect([...sourceSelectedKeys, ...targetSelectedKeys]);
  	}

  	doAnalysis() {
  		this.props.onAnalysis();
  	}

	render() {
	    const retVal = this.props.retVal;
	    const data = [];
		for (let i = 0; i < retVal.length; i++) {
			data.push({
			    key: i.toString(),
			    title: retVal[i]["name"]
		  	});
		}

	    return (
	    	<div>
				<Transfer
					dataSource={data}
					titles={['Source', 'Target']}
					targetKeys={this.props.targetKeys}
					selectedKeys={this.props.selectedKeys}
					onChange={this.doChange}
					onSelectChange={this.doChangeSelect}
					render={item => item.title} 
					listStyle={{ width: 240, height: 240 }}
		      	/>
	      		<Button type="primary" style={{ marginTop: 16, marginBottom: 48 }} onClick={this.doAnalysis}>Analysis</Button>
	      	</div>
    	);
	}
}