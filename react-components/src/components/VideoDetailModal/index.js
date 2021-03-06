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
  setActiveVideoDetailData,
  setActiveVideoDetailThumbnailAsPrimary,
  setFileSelectorVisible,
  updateActiveVideoDetailMetadata,
  openVideoDetailModal,
  closeVideoDetailModal,
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
  uploadingVideos, setActiveVideoDetailData, isVideoFileSelectorVisible,
  setFileSelectorVisible,
  updateActiveVideoDetailMetadata, openVideoDetailModal,
  closeVideoDetailModal, setActiveVideoDetailThumbnailAsPrimary,
}) => {
  const [_autogenThumbnailChoices, setAutogenThumbnailChoices] = useState(autogenThumbnailChoices);
  const [thumbsUpdatedFromUploadFeedback, setThumbsUpdatedFromUploadFeedback] = useState(false);
  const [isThumbnailUploading, setIsThumbUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isFileSelected, setIsFileSelected] = useState(false);
  const [percentageUploaded, setPercentageUploaded] = useState(0);
  // TODO: replace with uploadStatus, single var
  const [isProcessing, setIsProcessing] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isViewable, setIsViewable] = useState(false);

  // TODO: if isUploading=true, prevent leaving page.

  const [apiErrors, setApiErrors] = useState(null);
  const inputThumbnailFile = useRef(null);

  useEffect(() => {
    if (videoData.id) {
      setIsLoading(false);
      setAutogenThumbnailChoices(videoData.autogenThumbnailChoices);
    } else {
      setIsLoading(true);
    }
    if (uploadingVideos) {
      setIsUploading(true);
    }
    if (uploadingVideos && uploadingVideos[videoId] !== undefined && uploadingVideos[videoId] !== null) {
      if (uploadingVideos[videoId].isViewable !== undefined) {
        setIsUploading(uploadingVideos[videoId].isViewable);
        setIsViewable(uploadingVideos[videoId].isViewable);
        setIsProcessing(uploadingVideos[videoId].isProcessing === true);
      }

      if (uploadingVideos[videoId].isProcessing !== undefined) {
        setIsProcessing(uploadingVideos[videoId].isProcessing === true);
      }

      if (uploadingVideos[videoId].autogenThumbnailChoices && uploadingVideos[videoId].autogenThumbnailChoices.length >= 3) {
        if (!thumbsUpdatedFromUploadFeedback && uploadingVideos[videoId].autogenThumbnailChoices) {
          setAutogenThumbnailChoices(uploadingVideos[videoId].autogenThumbnailChoices);
          setThumbsUpdatedFromUploadFeedback(true);
        }
      }

      if (uploadingVideos[videoId].percentageUploaded) {
        setPercentageUploaded(uploadingVideos[videoId].percentageUploaded)
        if (uploadingVideos[videoId].percentageUploaded == 100) {
          setIsUploading(false);
        }
      }
    } else {
      setIsUploading(false);
      setIsProcessing(false);
      setIsViewable(true);
    }

  }, [videoData, uploadingVideos]);

  const updateParentState = (channelId) => {
    // Update the Channel Videos list on the page beneath
    console.log('>>>>>updateParentState');
    fetchActiveChannelVideos(channelId, false);
  };

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
    // TODO: readd this
    // setIsLoading(true);
    openVideoDetailModal(openedVideoId);
    // onSetModalOpen();
    setActiveVideoDetailData(openedVideoId);
    // const { data } = await getVideoById(videoId ? videoId : activeVideoId);
    // if (data) {
    //   setVideoData(data);
    //   setAutogenThumbnailChoices(getAutogenThumbnailChoices(data));
    // }
    // TODO: readd this
    // setIsLoading(false);
  };

  const handleInputThumbnailChange = async (e) => {
    const file = e.target.files[0];
    setIsThumbUploading(true);
    await updateVideoCustomThumbnail(videoData.id, file);

    setActiveVideoDetailData(videoData.id);
    // const { data } = await getVideoById(videoData.id);
    // if (data) {
    //   setVideoData(data);
    // }
    setIsThumbUploading(false);
    createToast(TOAST_PAYLOAD_VIDEO_DETAIL_SAVED);
    updateParentState(videoData.channel_id);
  };

  const handleFileSelect = async (acceptedFiles) => {
    // https://github.com/cvisionai/tator/blob/e7dd26489ab50637e480c22ded01673e27f5cad9/main/static/js/tasks/upload-worker.js
    // https://www.altostra.com/blog/multipart-uploads-with-s3-presigned-url
    console.debug('Video file was selected, starting upload...')
    setIsFileSelected(true);

    startVideoUpload(channelId, acceptedFiles[0]);
    setFileSelectorVisible(false);
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
        autogenThumbnailChoices={_autogenThumbnailChoices}
        percentageUploaded={percentageUploaded}
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
    createToast: createToast,
    setChannelSyncModalOpen: setChannelSyncModalOpen,
    fetchActiveChannelVideos: fetchActiveChannelVideos,
    startVideoUpload: startVideoUpload,
    setActiveVideoDetailData: setActiveVideoDetailData,
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
