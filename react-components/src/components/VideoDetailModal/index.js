import React, { useState, useRef, useEffect } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import VideoDetailModal from './VideoDetailModal';
import FileUploadChooseModal from './FileUploadChooseModal';

import {
  setChannelSyncModalOpenAction,
  fetchActiveChannelVideosAction,
  createToastAction,
  startVideoUploadAction,
  setActiveVideoDetailDataAction,
  setActiveVideoDetailThumbnailAsPrimaryAction,
  setFileSelectorVisibleAction,
  updateActiveVideoDetailMetadataAction,
  openVideoDetailModalAction,
  closeVideoDetailModalAction,
} from '../../actions/index';
import {
  getVideoById, updateVideoCustomThumbnail,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const TOAST_PAYLOAD_VIDEO_DETAIL_SAVED = {
  header: 'Success',
  body: 'Your video was saved',
};

const Container = ({
  videoId, autogenThumbnailChoices, videoData, channelId, fetchActiveChannelVideos, createToast,
  isModalOpen, startVideoUpload,
  uploadingVideos, setActiveVideoDetailData, isVideoFileSelectorVisible,
  setFileSelectorVisible,
  updateActiveVideoDetailMetadata, openVideoDetailModal,
  closeVideoDetailModal
}) => {
  // TODO: redux
  // const [activeVideoId, setActiveVideoId] = useState(videoId);
  const [isThumbnailUploading, setIsThumbUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isFileSelected, setIsFileSelected] = useState(false);
  const [percentageUploaded, setPercentageUploaded] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const [apiErrors, setApiErrors] = useState(null);
  const inputThumbnailFile = useRef(null);

  const updateParentState = (channelId) => {
    // Update the Channel Videos list on the page beneath
    fetchActiveChannelVideos(channelId, false);
  };

  const handleSetExistingThumbnailAsPrimary = async (videoRenditionThumbnailId) => {
    setIsThumbUploading(true);
    const videoId = setActiveVideoDetailData.id;
    setActiveVideoDetailThumbnailAsPrimary(videoId, videoRenditionThumbnailId);
    // const { data } = await setExistingThumbnailAsPrimary(videoId, videoRenditionThumbnailId);
    // setVideoData(data);
    setIsThumbUploading(false);
    // updateParentState(data.channel_id);
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
      updateActiveVideoDetailMetadata(videoData.id, updatedFields);
    }
  };

  const handleEditVideoModalOpen = async (openedVideoId = null) => {
    if (openedVideoId === null) {
      openedVideoId = videoId;
    }
    if (!videoId) {
      return null;
    }
    setIsLoading(true);
    openVideoDetailModalAction(openedVideoId);
    // onSetModalOpen();
    setActiveVideoDetailData(openedVideoId);
    // const { data } = await getVideoById(videoId ? videoId : activeVideoId);
    // if (data) {
    //   setVideoData(data);
    //   setAutogenThumbnailChoices(getAutogenThumbnailChoices(data));
    // }
    setIsLoading(false);
  };

  const handleInputThumbnailChange = async (e) => {
    const file = e.target.files[0];
    setIsThumbUploading(true);
    await updateVideoCustomThumbnail(setActiveVideoDetailData.id, file);
    const { data } = await getVideoById(setActiveVideoDetailData.id);
    if (data) {
      setVideoData(data);
    }
    setIsThumbUploading(false);
    createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SAVED);
    updateParentState(setActiveVideoDetailData.video.channel_id);
  };

  const handleFileSelect = async (acceptedFiles) => {
    // https://github.com/cvisionai/tator/blob/e7dd26489ab50637e480c22ded01673e27f5cad9/main/static/js/tasks/upload-worker.js
    // https://www.altostra.com/blog/multipart-uploads-with-s3-presigned-url
    console.debug('Video file was selected, starting upload...')
    setIsFileSelected(true);

    console.log('CALL 1');
    startVideoUpload(channelId, acceptedFiles[0]);
    setFileSelectorVisible(false);
    console.log('CALL 2');
    // // TODO: num files validation
    // const file = acceptedFiles[0]
    // const filename = file.name;
    // const fileSize = file.size;
    // const numParts = Math.ceil(fileSize / UPLOAD_CHUNK_SIZE)

    // setIsUploading(true);
    // const { response, data } = await uploadPrepare(channelId, filename, numParts);
    // setIsSaving(false);
    // if (response?.status === 400) {
    //   alert('upload error');
    // } else {
    //   console.debug(`Setting active videoId ${ data.video_id }`);
    //   setActiveVideoId(data.video_id);
    //   await uploadVideo(file, data);
    //   /*
    //   TODO:
    //   Call a function.
    //   If not video.is_viewable:

    //   - Every 10 seconds.
    //   - Call get video and update the video metadata for:
    //     - Auto gen thumbnails
    //     - primary thumbnail

    //   Store this in localstorage uploadFeedback object.

    //   If video.is_viewable:
    //    - Update the status to: Ready
    //   */

    //   setIsUploading(false);
    //   onSetModalOpen(true);
    //   setIsFileSelected(false);
    //   setShowFileSelect(false);
    // }

    // setIsUploading(false);
    // onSetModalOpen(true);
    // setIsFileSelected(false);
    // setShowFileSelect(false);

  }
  if (isVideoFileSelectorVisible === true) {
    return (
      <FileUploadChooseModal
        isFileSelected={isFileSelected}
        onFileSelect={handleFileSelect}
        // onModalClose={() => setIsChooseFileUploadModalOpen(false)}
        isModalOpen={isModalOpen}
        onModalOpen={() => handleEditVideoModalOpen}
        onModalClose={() => closeVideoDetailModal}
      />
    );
  } else {
    return (
      <VideoDetailModal
        inputThumbnailFile={inputThumbnailFile}
        isThumbnailUploading={isThumbnailUploading}
        isSaving={isSaving}
        isModalOpen={isModalOpen}
        isLoading={isLoading}
        videoData={videoData}
        autogenThumbnailChoices={autogenThumbnailChoices}
        percentageUploaded={percentageUploaded}
        isUploading={isUploading}
        apiErrors={apiErrors}
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
  let autogenThumbnailChoices = [];
  let videoData = null;
  let channelId = null;
  if (state.temp.activeVideoDetailData) {
    videoId = state.temp.activeVideoDetailData.id;
    autogenThumbnailChoices = state.temp.activeVideoDetailData.autogenThumbnailChoices;
    videoData = state.temp.activeVideoDetailData.video;
    channelId = state.temp.activeVideoDetailData.video.channel_id;
  } else {
    videoId = ownProps.videoId;
    videoData = null;
    channelId = ownProps.channelId;
  }
  return {
    uploadingVideos: state.temp.uploadingVideos,
    videoId: videoId,
    autogenThumbnailChoices: autogenThumbnailChoices,
    videoData: videoData,
    channelId: state.channels.activeChannelId,
    isVideoFileSelectorVisible: state.temp.isVideoFileSelectorVisible,
    isModalOpen: state.temp.isVideoDetailModalOpen,
  };
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    createToast: createToastAction,
    setChannelSyncModalOpen: setChannelSyncModalOpenAction,
    fetchActiveChannelVideos: fetchActiveChannelVideosAction,
    startVideoUpload: startVideoUploadAction,
    setActiveVideoDetailData: setActiveVideoDetailDataAction,
    setActiveVideoDetailThumbnailAsPrimary: setActiveVideoDetailThumbnailAsPrimaryAction,
    setFileSelectorVisible: setFileSelectorVisibleAction,
    openVideoDetailModal: openVideoDetailModalAction,
    closeVideoDetailModal: closeVideoDetailModalAction,
    updateActiveVideoDetailMetadata: updateActiveVideoDetailMetadataAction,
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
