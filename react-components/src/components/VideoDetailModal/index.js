import React, { useState, useRef, useEffect } from 'react';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import VideoDetailModal from './component';
import FileUploadChooseModal from './FileUploadChooseModal';

import {
  setChannelSyncModalOpen,
  fetchActiveChannelVideos,
  createToast,
  startVideoUpload,
  setVideoDetail,
  setActiveVideoDetailThumbnailAsPrimary,
  setFileSelectorVisible,
  updateActiveVideoDetailMetadata,
  openVideoDetailModal,
  closeVideoDetailModal,
  setVideoCustomThumbnail,
} from '../../actions/index';
import {
  updateVideoCustomThumbnail,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const TOAST_PAYLOAD_VIDEO_DETAIL_SAVED = {
  header: 'Success',
  body: 'Your video was saved',
};

const Container = ({
  videoId, autogenThumbnailChoices, videoData, channelId, fetchActiveChannelVideos, createToast,
  isModalOpen, startVideoUpload,
  uploadStatus, setVideoDetail, isVideoFileSelectorVisible,
  setFileSelectorVisible, videoDetailForm,
  updateActiveVideoDetailMetadata, openVideoDetailModal,
  closeVideoDetailModal, setActiveVideoDetailThumbnailAsPrimary, setVideoCustomThumbnail,
}) => {
  const [_autogenThumbnailChoices, setAutogenThumbnailChoices] = useState(autogenThumbnailChoices);
  const [thumbsUpdatedFromUploadFeedback, setThumbsUpdatedFromUploadFeedback] = useState(false);
  const [isThumbnailUploading, setIsThumbUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isFileSelected, setIsFileSelected] = useState(false);
  const [percentageUploaded, setPercentageUploaded] = useState(0);
  // TODO: replace with uploadStatus, single var
  console.log('uploadStatus');
  console.log(uploadStatus);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isViewable, setIsViewable] = useState(false);

  // TODO: if isUploading=true, prevent leaving page.

  const [apiErrors, setApiErrors] = useState(null);
  const inputThumbnailFile = useRef(null);

  // useEffect(() => {
  //   if (videoData.id) {
  //     setIsLoading(false);
  //     setAutogenThumbnailChoices(videoData.autogenThumbnailChoices);
  //   } else {
  //     setIsLoading(true);
  //   }
  //   if (uploadingVideos) {
  //     setIsUploading(true);
  //   }
  //   if (uploadingVideos && uploadingVideos[videoId] !== undefined && uploadingVideos[videoId] !== null) {
  //     if (uploadingVideos[videoId].isViewable !== undefined) {
  //       setIsUploading(uploadingVideos[videoId].isViewable);
  //       setIsViewable(uploadingVideos[videoId].isViewable);
  //       setIsProcessing(uploadingVideos[videoId].isProcessing === true);
  //     }

  //     if (uploadingVideos[videoId].isProcessing !== undefined) {
  //       setIsProcessing(uploadingVideos[videoId].isProcessing === true);
  //     }

  //     if (uploadingVideos[videoId].autogenThumbnailChoices && uploadingVideos[videoId].autogenThumbnailChoices.length >= 3) {
  //       if (!thumbsUpdatedFromUploadFeedback && uploadingVideos[videoId].autogenThumbnailChoices) {
  //         setAutogenThumbnailChoices(uploadingVideos[videoId].autogenThumbnailChoices);
  //         setThumbsUpdatedFromUploadFeedback(true);
  //       }
  //     }

  //     if (uploadingVideos[videoId].percentageUploaded) {
  //       setPercentageUploaded(uploadingVideos[videoId].percentageUploaded)
  //       if (uploadingVideos[videoId].percentageUploaded == 100) {
  //         setIsUploading(false);
  //       }
  //     }
  //   } else {
  //     setIsUploading(false);
  //     setIsProcessing(false);
  //     setIsViewable(true);
  //   }

  // }, [videoData, uploadingVideos]);

  const handleSetExistingThumbnailAsPrimary = async (videoRenditionThumbnailId) => {
    setIsThumbUploading(true);
    const videoId = videoData.id;
    await setActiveVideoDetailThumbnailAsPrimary(videoId, videoRenditionThumbnailId);
    setIsThumbUploading(false);
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
    if (!openedVideoId) {
      return null;
    }
    openVideoDetailModal(openedVideoId);
    setVideoDetail(openedVideoId);
  };

  const handleInputThumbnailChange = async (e) => {
    const file = e.target.files[0];
    setVideoCustomThumbnail(channelId, videoData.id, file);
  };

  const handleFileSelect = async (acceptedFiles) => {
    // https://github.com/cvisionai/tator/blob/e7dd26489ab50637e480c22ded01673e27f5cad9/main/static/js/tasks/upload-worker.js
    // https://www.altostra.com/blog/multipart-uploads-with-s3-presigned-url
    console.debug('Video file was selected, starting upload...')
    setIsFileSelected(true);
    startVideoUpload(channelId, acceptedFiles[0]);
    setFileSelectorVisible(false);
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
        autogenThumbnailChoices={_autogenThumbnailChoices}
        uploadStatus={uploadStatus}
        isUploading={isUploading}
        isProcessing={isProcessing}
        isViewable={isViewable}
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
  if (state.temp.videoDetail) {
    videoId = state.temp.videoDetail.id;
    autogenThumbnailChoices = state.temp.videoDetail.autogenThumbnailChoices;
    videoData = state.temp.videoDetail.video;
    channelId = state.temp.videoDetail.video.channel_id;
  } else {
    videoId = ownProps.videoId;
    videoData = null;
    channelId = ownProps.channelId;
  }
  return {
    uploadStatus: state.temp.uploadingVideos[videoId],
    // uploadingVideos: state.temp.uploadingVideos,
    videoId: videoId,
    autogenThumbnailChoices: autogenThumbnailChoices,
    videoData: videoData,
    channelId: state.channels.activeChannelId,
    isVideoFileSelectorVisible: state.temp.isVideoFileSelectorVisible,
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
    fetchActiveChannelVideos: fetchActiveChannelVideos,
    startVideoUpload: startVideoUpload,
    setVideoDetail: setVideoDetail,
    setActiveVideoDetailThumbnailAsPrimary: setActiveVideoDetailThumbnailAsPrimary,
    setFileSelectorVisible: setFileSelectorVisible,
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
