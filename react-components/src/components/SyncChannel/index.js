import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import SyncChannelButton from './component';

import {
  setChannelSyncModalOpen,
} from '../../actions/index';

// TODO: Call API
// import { syncChannelRequest } from '../../api/api';

const { store, persistor } = configureStore.getInstance();

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
    setChannelSyncModalOpen: setChannelSyncModalOpen,
  }, dispatch),
});

const mapStateToProps = (state) => ({
  isChannelSyncModalOpen: state.channels.isChannelSyncModalOpen,
});

export const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const CreateSyncChannelButtonContainer = ({
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
