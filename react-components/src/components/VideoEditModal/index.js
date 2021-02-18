import React, { useState, useRef, useEffect } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import VideoEditModal from './VideoEditModal';

import {
  setChannelSyncModalOpenAction,
  fetchActiveChannelVideosAction,
  createToastAction,
} from '../../actions/index';
import { MSG_CORRECT_FORM_ERRORS } from '../../constants';
import {
  getVideoById, updateVideo, updateVideoCustomThumbnail, setExistingThumbnailAsPrimary,
} from '../../api/api';
import { randomItem } from '../../utils';

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


const getAutogenThumbnailChoices = (videoData) => {
  let renditionThumbnails = [];
  if (videoData.video_renditions && videoData.video_renditions.length > 0) {
    // Find highest resolution rendition.
    const bestRendition = videoData.video_renditions.sort((a, b) => b.height - a.height)[0];
    renditionThumbnails = bestRendition.rendition_thumbnails;
  }
  if (renditionThumbnails.length > 0) {
    const thumb0 = randomItem(renditionThumbnails);
    const thumb1 = randomItem(renditionThumbnails);
    const thumb2 = randomItem(renditionThumbnails);
    return [
      [thumb0.id, thumb0.file],
      [thumb1.id, thumb1.file],
      [thumb2.id, thumb2.file],
    ];
  } else{
    return [];
  }
}

const Container = ({ videoId, fetchActiveChannelVideos, createToast, isModalOpen, onSetModalOpen, onSetModalClosed }) => {
  const [isThumbnailUploading, setIsThumbUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [videoData, setVideoData] = useState({});
  const [autogenThumbnailChoices, setAutogenThumbnailChoices] = useState([]);

  const [apiErrors, setApiErrors] = useState(null);
  const inputThumbnailFile = useRef(null);

  React.useEffect(async() => {
    if(isModalOpen) {
    await handleEditVideoModalOpen();
    }
  }, [isModalOpen]);

  const updateParentState = (channelId) => {
    // Update the Channel Videos list on the page beneath
    fetchActiveChannelVideos(channelId, false);
  };

  const handleSetExistingThumbnailAsPrimary = async (videoRenditionThumbnailId) => {
    setIsThumbUploading(true);
    const videoId = videoData.id;
    const { data } = await setExistingThumbnailAsPrimary(videoId, videoRenditionThumbnailId);
    setVideoData(data);
    setIsThumbUploading(false);
    updateParentState(data.channel_id);
  };

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
        updateParentState(data.channel_id);
      }
    }
  };

  const handleEditVideoModalOpen = async () => {
    console.log('handleEditVideoModalOpen');
    setIsLoading(true);
    onSetModalOpen();
    const { data } = await getVideoById(videoId);
    if (data) {
      setVideoData(data);
      setAutogenThumbnailChoices(getAutogenThumbnailChoices(data));
    }
    setIsLoading(false);
  };

  const handleInputThumbnailChange = async (e) => {
    const file = e.target.files[0];
    setIsThumbUploading(true);
    await updateVideoCustomThumbnail(videoData.id, file);
    const { data } = await getVideoById(videoData.id);
    if (data) {
      setVideoData(data);
    }
    setIsThumbUploading(false);
    createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SAVED);
    updateParentState(videoData.channel_id);
  };

  return (
    <VideoEditModal
      inputThumbnailFile={inputThumbnailFile}
      isThumbnailUploading={isThumbnailUploading}
      isSaving={isSaving}
      isModalOpen={isModalOpen}
      isLoading={isLoading}
      videoData={videoData}
      autogenThumbnailChoices={autogenThumbnailChoices}
      apiErrors={apiErrors}
      onModalOpen={() => handleEditVideoModalOpen}
      onModalClose={() => onSetModalClosed}
      onFormFieldChange={handleVideoUpdate}
      onInputThumbnailChange={handleInputThumbnailChange}
      onSetExistingThumbnailAsPrimary={handleSetExistingThumbnailAsPrimary}
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
export const VideoEditModalContainer = ({
  element,
  ...params
}) => (
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <ConnectedContainer {...params} />
    </PersistGate>
  </Provider>
);
