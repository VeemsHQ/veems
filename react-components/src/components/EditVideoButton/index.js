import React, { useState } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import EditVideoButton from './EditVideoButton';

import {
  setChannelSyncModalOpenAction,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();

const Container = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const handleSyncChannel = () => {
    // todo when server calls in place
    // syncChannelRequest();
  };

  const handleEditVideoModalClose = () => {
    setModalOpen(false);
  };
  const handleEditVideoModalOpen = () => {
    setModalOpen(true);
  };

  return (
    <EditVideoButton
      isModalOpen={modalOpen}
      onSyncChannel={handleSyncChannel}
      onModalOpen={() => handleEditVideoModalOpen}
      onModalClose={() => handleEditVideoModalClose}
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
});

export const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

// NOTE: This does not render to the DOM like other components.
export const EditVideoButtonContainer = ({
  element,
  ...params
}) => (
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <ConnectedContainer {...params} />
    </PersistGate>
  </Provider>
);
