import React, { useState } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import EditVideoButton from './EditVideoButton';

import {
  setChannelSyncModalOpenAction,
  fetchActiveChannelVideosAction,
} from '../../actions/index';
import { getVideoById, updateVideo } from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const Container = ({ videoId, fetchActiveChannelVideos }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [videoData, setVideoData] = useState({});
  const [apiErrors, setApiErrors] = useState(null);

  const handleVideoUpdate = async (videoData, updatedFields) => {
    // To give better UX, update the state before the server request.
    setIsSaving(true);
    let newData = Object.create(videoData);
    newData = Object.assign(newData, updatedFields);
    setVideoData(newData);
    // Now do it for real.
    const { response, data } = await updateVideo(videoId, updatedFields);
    if (response?.status === 400) {
      setApiErrors(response?.data);
      setIsSaving(false);
    } else {
      setApiErrors(null);
      setVideoData(data);
      setIsSaving(false);
      // Update the Channel Videos list on the page beneath
      await fetchActiveChannelVideos(videoData.channel_id, false);
    }
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
      apiErrors={apiErrors}
      onModalOpen={() => handleEditVideoModalOpen}
      onModalClose={() => handleEditVideoModalClose}
      onFormFieldChange={handleVideoUpdate}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    setChannelSyncModalOpen: setChannelSyncModalOpenAction,
    fetchActiveChannelVideos: fetchActiveChannelVideosAction,
  }, dispatch),
});

export const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

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
