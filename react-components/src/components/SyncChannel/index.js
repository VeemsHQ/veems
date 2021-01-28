import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import SyncChannelButton from './SyncChannelButton';

import {
  setChannelSyncModalOpenAction,
} from '../../actions/index';

// api
// import { syncChannelRequest } from '../../api/api';

const { store, persistor } = configureStore.getInstance();

// Component connected to Redux store
const Container = ({
  isChannelSyncModalOpen,
  setChannelSyncModalOpen,
}) => {
  const handleSyncChannel = () => {
    // todo when server calls in place
    // syncChannelRequest();
  };
  const handleModalClose = () => setChannelSyncModalOpen(false);
  const handleModalOpen = () => setChannelSyncModalOpen(true);
  return (
    <SyncChannelButton
      isModalOpen={isChannelSyncModalOpen}
      onSyncChannel={handleSyncChannel}
      onModalOpen={() => handleModalOpen}
      onModalClose={() => handleModalClose}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    setChannelSyncModalOpen: setChannelSyncModalOpenAction,
  }, dispatch),
});

const mapStateToProps = (state) => ({
  isChannelSyncModalOpen: state.channels.isChannelSyncModalOpen,
});

export const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const SyncChannelContainer = ({
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
