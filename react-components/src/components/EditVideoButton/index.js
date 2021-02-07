import React, { useState } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import EditVideoButton from './EditVideoButton';

import {
  setChannelSyncModalOpenAction,
} from '../../actions/index';
import { getVideoById } from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const Container = ({ videoId }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [videoData, setVideoData] = useState(null);
  const handleSyncChannel = () => {
    // todo when server calls in place
    // syncChannelRequest();
  };

  const handleEditVideoModalClose = () => {
    setModalOpen(false);
    setIsLoading(true);
  };
  const handleEditVideoModalOpen = async () => {
    setModalOpen(true);
    const videoResponse = await getVideoById(videoId);
    setVideoData(videoResponse.data);
    setIsLoading(false);
  };

  console.log('fed1');
  console.log(videoData);
  console.log('fed2');

  return (
    <EditVideoButton
      isModalOpen={modalOpen}
      isLoading={isLoading}
      videoData={videoData}
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
