import React, { useState, useRef, useEffect } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import VideoDetailModal from './component';
import FileUploadChooseModal from './FileUploadChooseModal';

import {
  setChannelSyncModalOpen,
  setActiveChannel,
  createToast,
  startVideoUpload,
  setVideoDetail,
  setActiveVideoDetailThumbnailAsPrimary,
  updateActiveVideoDetailMetadata,
  openVideoDetailModal,
  closeVideoDetailModal,
  setVideoCustomThumbnail,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();

const TOAST_PAYLOAD_VIDEO_DETAIL_SAVED = {
  header: 'Success',
  body: 'Your video was saved',
};

const Container = ({
  videoId, videoDetail, channelId, createToast,
  isModalOpen, startVideoUpload,
  uploadStatus, setVideoDetail,
  videoDetailForm, channels, setActiveChannel,
  updateActiveVideoDetailMetadata, openVideoDetailModal,
  closeVideoDetailModal, setActiveVideoDetailThumbnailAsPrimary, setVideoCustomThumbnail,
}) => {
  const [isSaving, setIsSaving] = useState(false);
  // TODO: if isUploading=true, prevent leaving page.
  // const [apiErrors, setApiErrors] = useState(null);
  const inputThumbnailFile = useRef(null);

  const handleSetExistingThumbnailAsPrimary = async (videoRenditionThumbnailId) => {
    const videoId = videoDetail.id;
    await setActiveVideoDetailThumbnailAsPrimary(videoId, videoRenditionThumbnailId);
  };

  const handleVideoUpdate = async (video, updatedFields = null) => {
    // To give better UX, update the state before the server request.
    setIsSaving(true);
    if (!updatedFields) {
      // If no fields updated, pretend to do it.
      await new Promise((r) => setTimeout(r, 300));
      createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SAVED);
      setIsSaving(false);
    } else {
      // Now do it for real.
      let newData = Object.create(video);
      newData = Object.assign(newData, updatedFields);
      updateActiveVideoDetailMetadata(video.id, updatedFields);
    }
  };

  const handleEditVideoModalOpen = async (openedVideoId = null) => {
    if (openedVideoId === null) {
      openedVideoId = videoId;
    }
    if (!openedVideoId) {
      return null;
    }
    openVideoDetailModal(openedVideoId);
    setVideoDetail(openedVideoId);
  };

  const handleInputThumbnailChange = async (e) => {
    const file = e.target.files[0];
    setVideoCustomThumbnail(channelId, videoDetail.id, file);
  };

  const handleFileSelect = async (acceptedFiles) => {
    console.debug('Video file was selected, starting upload...')
    // TODO: validate only one file is selected.
    // TODO: validate it's a video file.
    // TODO: validate file size.
    startVideoUpload(channelId, acceptedFiles[0]);
  }
  if (videoDetailForm.isFileSelectorVisible === true) {
    return (
      <FileUploadChooseModal
        isFileSelected={videoDetailForm.isFileSelected}
        onFileSelect={handleFileSelect}
        // onModalClose={() => setIsChooseFileUploadModalOpen(false)}
        isModalOpen={isModalOpen}
        channels={channels}
        channelId={channelId}
        setActiveChannel={setActiveChannel}
        onModalOpen={() => handleEditVideoModalOpen}
        onModalClose={() => closeVideoDetailModal}
      />
    );
  } else {
    return (
      <VideoDetailModal
        inputThumbnailFile={inputThumbnailFile}
        isModalOpen={isModalOpen}
        videoDetail={videoDetail}
        videoDetailForm={videoDetailForm}
        uploadStatus={uploadStatus}
        onModalOpen={(videoId) => handleEditVideoModalOpen(videoId)}
        onModalClose={() => closeVideoDetailModal}
        onFormFieldChange={handleVideoUpdate}
        onInputThumbnailChange={handleInputThumbnailChange}
        onSetExistingThumbnailAsPrimary={handleSetExistingThumbnailAsPrimary}
      />
    );
  }
};

const mapStateToProps = (state, ownProps) => {
  let videoId = null;
  let channels = [];
  if (ownProps.channels && !state.channels.channels.length) {
    channels = ownProps.channels;
  } else {
    channels = state.channels.channels;
  }
  if (state.temp.videoDetail.video.id) {
    videoId = state.temp.videoDetail.video.id;
  } else {
    videoId = ownProps.videoId;
  }
  return {
    uploadStatus: state.temp.uploadingVideos[videoId],
    videoId: videoId,
    videoDetail: state.temp.videoDetail,
    channelId: state.channels.activeChannelId,
    channels: channels,
    isModalOpen: state.temp.isVideoDetailModalOpen,
    videoDetailForm: state.temp.videoDetailForm,
  };
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    setVideoCustomThumbnail: setVideoCustomThumbnail,
    createToast: createToast,
    setChannelSyncModalOpen: setChannelSyncModalOpen,
    setActiveChannel: setActiveChannel,
    startVideoUpload: startVideoUpload,
    setVideoDetail: setVideoDetail,
    setActiveVideoDetailThumbnailAsPrimary: setActiveVideoDetailThumbnailAsPrimary,
    openVideoDetailModal: openVideoDetailModal,
    closeVideoDetailModal: closeVideoDetailModal,
    updateActiveVideoDetailMetadata: updateActiveVideoDetailMetadata,
  }, dispatch),
});

export const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

// NOTE: This does not render to the DOM like other components.
export const VideoDetailModalContainer = ({
  element,
  ...params
}) => (
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <ConnectedContainer {...params} />
    </PersistGate>
  </Provider>
);
