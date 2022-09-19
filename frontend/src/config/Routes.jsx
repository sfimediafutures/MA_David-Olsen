import React from 'react';

import { Route, Switch } from 'react-router-dom';

import Home from '../pages/Home';
import Catalog from '../pages/Catalog';
import Detail from '../pages/detail/Detail';
import Upload from '../pages/features/Upload';

const Routes = () => {
    return (
        <Switch>
            <Route
                path='/upload'
                exact
                component={Upload}
            />
            <Route
                path='/:category/search/:keyword'
                component={Catalog}
            />
            <Route
                path='/:category/:id'
                component={Detail}
            />
            <Route
                path='/'
                exact
                component={Home}
            />
            
            <Route
                path='/:category'
                component={Catalog}
            />
        </Switch>
    );
}

export default Routes;

