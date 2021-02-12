import React, { useState, useRef } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import EditVideoButton from './EditVideoButton';

import {
  setChannelSyncModalOpenAction,
  fetchActiveChannelVideosAction,
  createToastAction,
} from '../../actions/index';
import { MSG_CORRECT_FORM_ERRORS } from '../../constants';
import { getVideoById, updateVideo, updateVideoCustomThumbnail } from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const TOAST_PAYLOAD_VIDEO_DETAIL_SAVED = {
  header: 'Success',
  body: 'Your video was saved',
};
const TOAST_PAYLOAD_VIDEO_DETAIL_BAD_INPUT = {
  header: 'Oops',
  body: MSG_CORRECT_FORM_ERRORS,
  isError: true,
};

const Container = ({ videoId, fetchActiveChannelVideos, createToast }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [isThumbnailUploading, setIsThumbUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [videoData, setVideoData] = useState({});
  const [apiErrors, setApiErrors] = useState(null);
  const inputThumbnailFile = useRef(null);

  const handleVideoUpdate = async (videoData, updatedFields = null) => {
    // To give better UX, update the state before the server request.
    setIsSaving(true);
    if (!updatedFields) {
      // If no fields updated, pretend to do it.
      await new Promise((r) => setTimeout(r, 300));
      createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SAVED);
      setIsSaving(false);
    } else {
      // Now do it for real.
      let newData = Object.create(videoData);
      newData = Object.assign(newData, updatedFields);
      setVideoData(newData);
      const { response, data } = await updateVideo(videoData.id, updatedFields);
      setIsSaving(false);
      if (response?.status === 400) {
        createToast(TOAST_PAYLOAD_VIDEO_DETAIL_BAD_INPUT);
        setApiErrors(response?.data);
      } else {
        createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SAVED);
        setApiErrors(null);
        setVideoData(data);
        // Update the Channel Videos list on the page beneath
        await fetchActiveChannelVideos(videoData.channel_id, false);
      }
    }
  };

  const handleEditVideoModalClose = () => {
    setModalOpen(false);
    setIsLoading(true);
  };

  const handleEditVideoModalOpen = async () => {
    setModalOpen(true);
    const { data } = await getVideoById(videoId);
    if (data) {
      setVideoData(data);
    }
    setIsLoading(false);
  };

  const handleInputThumbnailChange = async (e) => {
    console.log(e.target.files);
    const file = e.target.files[0];
    setIsThumbUploading(true);
    await updateVideoCustomThumbnail(videoData.id, file);
    const { data } = await getVideoById(videoData.id);
    if (data) {
      setVideoData(data);
    }
    setIsThumbUploading(false);
    // Update the Channel Videos list on the page beneath
    await fetchActiveChannelVideos(videoData.channel_id, false);
  };

  return (
    <EditVideoButton
      inputThumbnailFile={inputThumbnailFile}
      isThumbnailUploading={isThumbnailUploading}
      isSaving={isSaving}
      isModalOpen={modalOpen}
      isLoading={isLoading}
      videoData={videoData}
      apiErrors={apiErrors}
      onModalOpen={() => handleEditVideoModalOpen}
      onModalClose={() => handleEditVideoModalClose}
      onFormFieldChange={handleVideoUpdate}
      onInputThumbnailChange={handleInputThumbnailChange}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    createToast: createToastAction,
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
