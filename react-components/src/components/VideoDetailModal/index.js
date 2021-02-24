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
} from '../../actions/index';
import { MSG_CORRECT_FORM_ERRORS } from '../../constants';
import {
  getVideoById, updateVideo, updateVideoCustomThumbnail, setExistingThumbnailAsPrimary,
  uploadPrepare, uploadVideoParts, uploadComplete,
} from '../../api/api';
import { randomItem } from '../../utils';

const { store, persistor } = configureStore.getInstance();

const UPLOAD_CHUNK_SIZE = 5 * 1024 * 1024;
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
  } else {
    return [];
  }
}

const Container = ({ videoId = null, channelId, fetchActiveChannelVideos, createToast, isModalOpen, onSetModalOpen, onSetModalClosed }) => {
  const [activeVideoId, setActiveVideoId] = useState(videoId);
  const [showFileSelect, setShowFileSelect] = useState(isModalOpen && !videoId);
  const [isThumbnailUploading, setIsThumbUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [isFileSelected, setIsFileSelected] = useState(false);
  const [videoData, setVideoData] = useState({});
  const [autogenThumbnailChoices, setAutogenThumbnailChoices] = useState([]);
  const [percentageUploaded, setPercentageUploaded] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const [apiErrors, setApiErrors] = useState(null);
  const inputThumbnailFile = useRef(null);

  React.useEffect(async () => {
    setShowFileSelect(isModalOpen && !activeVideoId);
    if (videoId) {
      setActiveVideoId(videoId);
      setShowFileSelect(isModalOpen && !videoId);
      if (isModalOpen && activeVideoId) {
        await handleEditVideoModalOpen(videoId);
      }
    } else {
      if (isModalOpen && activeVideoId) {
        await handleEditVideoModalOpen();
        setShowFileSelect(isModalOpen && !activeVideoId);
      }
    }
  }, [isModalOpen, activeVideoId, videoId]);

  // React.useEffect(async () => {
  //   console.log(`isModalOpen: ${videoId}`)
  //   console.log(`videoId: ${videoId}`)
  //   setActiveVideoId(videoId)
  //   if (isModalOpen && videoId) {
  //     await handleEditVideoModalOpen(videoId);
  //   }
  //   setShowFileSelect(isModalOpen && !videoId);
  // }, [isModalOpen, videoId]);

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
      setActiveVideoId(videoData.id);
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

  const handleEditVideoModalOpen = async (videoId = null) => {
    setIsLoading(true);
    onSetModalOpen();
    const { data } = await getVideoById(videoId ? videoId : activeVideoId);
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

  const updateUploadProgress = async (percentageDone) => {
    console.debug(`Upload progress updated: ${percentageDone}`);
    setPercentageUploaded(percentageDone);
  }

  const uploadVideo = async (file, uploadPrepareResult) => {
    updateUploadProgress(0);
    const fileSize = file.size;
    const numParts = Math.ceil(fileSize / UPLOAD_CHUNK_SIZE)
    const uploadId = uploadPrepareResult.upload_id;
    const presignedUploadUrls = uploadPrepareResult.presigned_upload_urls;
    console.debug('Uploading video parts')
    const parts = await uploadVideoParts(
      presignedUploadUrls,
      file,
      numParts,
      fileSize,
      UPLOAD_CHUNK_SIZE,
      updateUploadProgress,
    )
    console.debug('Uploading video parts completed')
    await uploadComplete(uploadId, parts);
  }

  const handleFileSelect = async (acceptedFiles) => {
    // https://github.com/cvisionai/tator/blob/e7dd26489ab50637e480c22ded01673e27f5cad9/main/static/js/tasks/upload-worker.js
    // https://www.altostra.com/blog/multipart-uploads-with-s3-presigned-url
    console.debug('Video file was selected, starting upload...')
    setIsFileSelected(true);
    // TODO: num files validation
    const file = acceptedFiles[0]
    const filename = file.name;
    const fileSize = file.size;
    const numParts = Math.ceil(fileSize / UPLOAD_CHUNK_SIZE)

    setIsUploading(true);
    const { response, data } = await uploadPrepare(channelId, filename, numParts);
    setIsSaving(false);
    if (response?.status === 400) {
      alert('upload error');
    } else {
      console.debug(`Setting active videoId ${data.video_id}`);
      setActiveVideoId(data.video_id);
      await uploadVideo(file, data);
      /*
      TODO:
      Call a function.
      If not video.is_viewable:

      - Every 10 seconds.
      - Call get video and update the video metadata for:
        - Auto gen thumbnails
        - primary thumbnail

      Store this in localstorage uploadFeedback object.

      If video.is_viewable:
       - Update the status to: Ready
      */

      setIsUploading(false);
      onSetModalOpen(true);
      setIsFileSelected(false);
      setShowFileSelect(false);
    }

  }
  if (showFileSelect === true) {
    return (
      <FileUploadChooseModal
        isFileSelected={isFileSelected}
        onFileSelect={handleFileSelect}
        // onModalClose={() => setIsChooseFileUploadModalOpen(false)}
        isModalOpen={true}
        onModalOpen={() => handleEditVideoModalOpen}
        onModalClose={() => onSetModalClosed}
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
        onModalOpen={() => handleEditVideoModalOpen}
        onModalClose={() => onSetModalClosed}
        onFormFieldChange={handleVideoUpdate}
        onInputThumbnailChange={handleInputThumbnailChange}
        onSetExistingThumbnailAsPrimary={handleSetExistingThumbnailAsPrimary}
      />
    );
  }
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
