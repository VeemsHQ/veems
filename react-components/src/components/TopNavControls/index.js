import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import TopNavControls from './component';

import {
    openUploadVideoModal,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();

function Container({
    openUploadVideoModal,
}) {
    const onOpenUploadVideoModalClicked = async (e) => {
        if (window.location.pathname == '/channel/videos/') {
            e.preventDefault();
            openUploadVideoModal();
        } else {
            console.debug('Upload clicked, not on Channel Managed Videos page, redirecting...');
        }
    }
    return (
        <TopNavControls
            openUploadVideoModal={onOpenUploadVideoModalClicked}
        />
    );
}

const mapDispatchToProps = (dispatch) => ({
    dispatch,
    ...bindActionCreators({
        openUploadVideoModal: openUploadVideoModal,
    }, dispatch),
});

const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

export const CreateTopNavControls = ({
    element,
    ...params
}) => (
    ReactDOM.render(
        <Provider store={store}>
            <PersistGate loading={null} persistor={persistor}>
                <ConnectedContainer {...params} />
            </PersistGate>
        </Provider>,
        element,
    )
);
