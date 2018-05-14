'use strict';
import {
  HashRouter as Router,
  Route,
  Link,
  Redirect
} from 'react-router-dom';

import HomePage from './components/HomePage.js'
import DetailPage from './components/DetailPage.js'
import AdminPage from './components/admin/AdminPage.js'
import SdkPage from './components/sdk/SdkPage.js'


ReactDOM.render((
	<Router>
		<div>
			<Route exact path="/" component={HomePage} />
			<Route path="/detail/:id/" component={DetailPage} />
			<Route path="/debug" component={AdminPage} />
			<Route path="/sdk" component={SdkPage} />
		</div>
	</Router>
), document.getElementById('root'));