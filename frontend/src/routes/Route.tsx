import React from 'react';
import { 
    Route as ReactDOMRoute,
    RouteProps as ReactDOMRouteProps,
    Redirect,
 } from "react-router-dom";

import { useAuth } from '../context/AuthContext';

interface RouteProps extends ReactDOMRouteProps {
    isPrivate?: boolean;
    component: React.ComponentType;
}

const Route: React.FC<RouteProps> = ({
    isPrivate = false,
    component: Component,
    ...rest
}) => {
    const { user } = useAuth();

    return (
        <ReactDOMRoute
            {...rest}
            render={() => {
                return isPrivate === !!user ? (
                    <Component />
                ) : (
                    <Redirect to={{ pathname: isPrivate ? '/' : '/agendas' }} />
                );
            }}
        />
    );
};

export default Route;