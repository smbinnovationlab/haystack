'use strict';

const pageHeight = document.body.clientHeight;


export default class HomePageChart extends React.Component {
	constructor(props) {
		super(props);
		this.state = {};
	}

	render() {
		return (
			<div style={{height: (pageHeight - 92) / 2}}></div>
		);
	}
}