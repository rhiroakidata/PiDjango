import React from 'react';
import { Switch } from 'react-router-dom';

import Route from './Route';

import SignIn from '../pages/SignIn';
import SignUp from "../pages/SignUp";
import Agendas from '../pages/Agendas';

const Routes: React.FC = () => (
    <Switch>
        <Route path='/' exact component={SignIn} />
        <Route path='/signup' component={SignUp} />
        <Route path='/agendas' component={Agendas} isPrivate />        
    </Switch>
);

export default Routes;