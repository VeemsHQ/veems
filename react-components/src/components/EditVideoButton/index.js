import React, { useState } from 'react';

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
import { MSG_SERVER_ERROR, MSG_CORRECT_FORM_ERRORS } from '../../constants';
import { getVideoById, updateVideo } from '../../api/api';

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
const TOAST_PAYLOAD_VIDEO_DETAIL_SERVER_ERROR = {
  header: 'Oops',
  body: MSG_SERVER_ERROR,
  isError: true,
};

const Container = ({ videoId, fetchActiveChannelVideos, createToast }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [videoData, setVideoData] = useState({});
  const [apiErrors, setApiErrors] = useState(null);

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
      if (response?.status >= 500) {
        setIsSaving(false);
        createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SERVER_ERROR);
      } else if (response?.status === 400) {
        createToast(TOAST_PAYLOAD_VIDEO_DETAIL_BAD_INPUT);
        setApiErrors(response?.data);
        setIsSaving(false);
      } else {
        createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SAVED);
        setApiErrors(null);
        setVideoData(data);
        setIsSaving(false);
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
    const { response, data } = await getVideoById(videoId);
    if (response?.status >= 500) {
      createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SERVER_ERROR);
    } else {
      setVideoData(data);
    }
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
