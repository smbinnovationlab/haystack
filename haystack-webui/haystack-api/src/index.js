'use strict';
import {
  HashRouter as Router,
  Route,
  Link,
  Redirect
} from 'react-router-dom';

import SdkPage from './components/SdkPage.js'


ReactDOM.render((
	<Router>
		<div>
			<Route exact path="/" component={SdkPage} />
		</div>
	</Router>
), document.getElementById('root'));