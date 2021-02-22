import React, { useState, useRef } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import DeleteVideoButton from './DeleteVideoButton';

import {
  fetchActiveChannelVideosAction,
  createToastAction,
} from '../../actions/index';
import { MSG_CORRECT_FORM_ERRORS } from '../../constants';
import {
  getVideoById, deleteVideo,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const TOAST_SUCCESS_PAYLOAD = {
  header: 'Success',
  body: 'Video deleted',
};
const TOAST_BAD_REQUEST_PAYLOAD = {
  header: 'Oops',
  body: MSG_CORRECT_FORM_ERRORS,
  isError: true,
};

const Container = ({ videoId, fetchActiveChannelVideos, createToast }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [videoData, setVideoData] = useState({});

  const updateParentState = (channelId) => {
    // Update the Channel Videos list on the page beneath
    fetchActiveChannelVideos(channelId, false);
  };

  const handleDelete = async (e) => {
    e.preventDefault();
    const videoId = videoData.id;
    if (videoId === undefined) {
      console.warning('no video on delete');
      console.warning(videoData);
    }
    setIsSaving(true);
    const { response } = await deleteVideo(videoId);
    updateParentState(videoData.channel_id);
    setIsSaving(false);
    setModalOpen(false);
    if (response?.status === 400) {
      createToast(TOAST_BAD_REQUEST_PAYLOAD);
    } else {
      createToast(TOAST_SUCCESS_PAYLOAD);
      setVideoData({});
    }
  };

  const handleDeleteVideoModalClose = () => {
    setModalOpen(false);
    setIsLoading(false);
  };

  const handleDeleteVideoModalOpen = async () => {
    setModalOpen(true);
    setIsLoading(true);
    const { data } = await getVideoById(videoId);
    if (data) {
      setVideoData(data);
    }
    setIsLoading(false);
  };

  return (
    <DeleteVideoButton
      isSaving={isSaving}
      isModalOpen={modalOpen}
      isLoading={isLoading}
      videoData={videoData}
      onModalOpen={() => handleDeleteVideoModalOpen}
      onModalClose={() => handleDeleteVideoModalClose}
      onDelete={() => handleDelete}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    createToast: createToastAction,
    fetchActiveChannelVideos: fetchActiveChannelVideosAction,
  }, dispatch),
});

export const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

// NOTE: This does not render to the DOM like other components.
export const DeleteVideoButtonContainer = ({
  element,
  ...params
}) => (
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <ConnectedContainer {...params} />
    </PersistGate>
  </Provider>
);
