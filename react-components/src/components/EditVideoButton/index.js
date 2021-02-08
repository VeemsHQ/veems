import React, { useState } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import EditVideoButton from './EditVideoButton';

import {
  setChannelSyncModalOpenAction,
} from '../../actions/index';
import { getVideoById, updateVideo } from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const Container = ({ videoId }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [videoData, setVideoData] = useState({});

  const handleVideoUpdate = async (updatedFields) => {
    // To give better UX, update the state before the server request.
    setIsSaving(true);
    let newData = Object.create(videoData);
    newData = Object.assign(newData, updatedFields);
    setVideoData(newData);
    // Now do it for real.
    const videoResponse = await updateVideo(videoId, updatedFields);
    setVideoData(videoResponse.data);
    setIsSaving(false);
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

  return (
    <EditVideoButton
      isSaving={isSaving}
      isModalOpen={modalOpen}
      isLoading={isLoading}
      videoData={videoData}
      onModalOpen={() => handleEditVideoModalOpen}
      onModalClose={() => handleEditVideoModalClose}
      handleChange={handleVideoUpdate}
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
