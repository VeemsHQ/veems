import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import Logout from './component';
import {
    destroySession,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();

const Container = ({
    destroySession,
}) => {
    return (
        <Logout destroySession={destroySession} />
    );
};

const mapDispatchToProps = (dispatch) => ({
    dispatch,
    ...bindActionCreators({
        destroySession: destroySession,
    }, dispatch),
});

const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

export const CreateLogoutContainer = ({
    element,
    ...params
}) => (
    ReactDOM.render(
        <Provider store={store}>
            <PersistGate loading={null} persistor={persistor}>
                <ConnectedContainer {...params} />
            </PersistGate>
        </Provider>,
        element || document.createElement('div'), // for testing purposes
    )
);
