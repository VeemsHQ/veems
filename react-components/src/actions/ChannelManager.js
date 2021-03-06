import * as aTypes from './ActionTypes';
import {
  uploadVideoParts,
  uploadComplete,
  uploadPrepare,
  getVideoById,
  setExistingThumbnailAsPrimary,
  updateVideo,
  getUploadById,
  createChannelRequest,
  getChannelsRequest,
} from '../api/api';
import { MSG_CORRECT_FORM_ERRORS } from '../constants';
import { configureStore } from '../store';
import { randomItem } from '../utils';
import { fetchActiveChannelVideos, setChannels, setActiveChannel } from './Channel';
import { createToast } from './Global';

const { store } = configureStore.getInstance();

const _setCreateChannelApiErrors = apiErrors => ({
  type: aTypes.SET_CREATE_CHANNEL_API_ERRORS,
  payload: apiErrors
})

const _setCreateChannelShowModal = bool => ({
  type: aTypes.SET_CREATE_CHANNEL_SHOW_MODAL,
  payload: bool
})

const _setVideoDetail = videoDetail => ({
  type: aTypes.SET_VIDEO_DETAIL,
  payload: videoDetail
})

const _setVideoDetailModalOpen = bool => ({
  type: aTypes.SET_VIDEO_DETAIL_MODAL_OPEN,
  payload: bool
})

const _setVideoUploadingFeedback = feedback => ({
  type: aTypes.SET_VIDEO_UPLOADING_FEEDBACK,
  payload: feedback
})

export const setChannelSyncModalOpen = (state) => async (dispatch) => {
  console.debug('action, setChannelSyncModalOpen');
  dispatch({ type: aTypes.SET_CHANNEL_SYNC_MODAL_OPEN, payload: state });
};

export const updateActiveVideoDetailMetadata = (videoId, updatedFields) => async (dispatch) => {
  const { response, data } = await updateVideo(videoId, updatedFields);
  if (response?.status === 400) {
    // setApiErrors(response?.data);
    dispatch(createToast({
      header: 'Oops',
      body: MSG_CORRECT_FORM_ERRORS,
      isError: true,
    }));
  } else {
    dispatch(createToast({
      header: 'Success',
      body: 'Your video was saved',
    }));
    // setApiErrors(null);
    dispatch(_setVideoDetail(data));
    dispatch(fetchActiveChannelVideos(data.channel_id, false));
  }
}

export const openVideoDetailModal = (videoId) => async (dispatch) => {
  console.log(`openVideoDetailModal: ${videoId}`);
  dispatch(setVideoDetail(videoId));
  dispatch(_setVideoDetailModalOpen(true));
}

export const closeVideoDetailModal = () => async (dispatch) => {
  dispatch(_setVideoDetailModalOpen(false));
}

export const setVideoDetail = (videoId) => async (dispatch) => {
  console.debug('action, setVideoDetail');
  const { data } = await getVideoById(videoId);
  dispatch(_setVideoDetail(data));
};

export const setActiveVideoDetailThumbnailAsPrimary = (videoId, videoRenditionThumbnailId) => async (dispatch) => {
  console.debug('action, setActiveVideoDetailThumbnailAsPrimary');
  const { data } = await setExistingThumbnailAsPrimary(videoId, videoRenditionThumbnailId);
  dispatch(fetchActiveChannelVideos(data.channel_id, false));
  dispatch(_setVideoDetail(data));
};

export const setFileSelectorVisible = (bool) => async (dispatch) => {
  console.debug('action, setFileSelectorVisible');
  dispatch({ type: aTypes.SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTOR_VISIBLE, payload: bool });
}

const _updateUploadProgress = async (percentageDone) => {
  console.debug(`Upload progress updated: ${percentageDone}`);
  const feedback = {
    percentageUploaded: percentageDone
  };
  store.dispatch(_setVideoUploadingFeedback(feedback));
  // store.dispatch({ type: aTypes.SET_VIDEO_UPLOADING_FEEDBACK, payload: feedback });
  // TODO: get the video
}

const _uploadVideo = async (file, uploadPrepareResult) => {
  const chunkSize = 5 * 1024 * 1024; // 5MB
  const fileSize = file.size;
  const numParts = Math.ceil(fileSize / chunkSize)
  const uploadId = uploadPrepareResult.upload_id;
  const presignedUploadUrls = uploadPrepareResult.presigned_upload_urls;
  console.debug('Uploading video parts')
  const parts = await uploadVideoParts(
    presignedUploadUrls,
    file,
    numParts,
    fileSize,
    chunkSize,
    _updateUploadProgress,
  )
  console.debug('Uploading video parts completed')
  await uploadComplete(uploadId, parts);
}

export const startVideoUpload = (channelId, file) => async (dispatch) => {
  console.debug('action, startVideoUpload');
  const chunkSize = 5 * 1024 * 1024; // 5MB
  const filename = file.name;
  const fileSize = file.size;
  const numParts = Math.ceil(fileSize / chunkSize);

  const { response, data } = await uploadPrepare(channelId, filename, numParts);
  if (response?.status === 400) {
    console.error('UPLOAD FAILED');
  } else {
    dispatch({ type: aTypes.START_VIDEO_UPLOADING, payload: data.video_id });
    dispatch(provideUploadFeedback(data.video_id, data.upload_id, channelId));
    dispatch(setVideoDetail(data.video_id));
    await _uploadVideo(file, data);
  }
};

const provideUploadFeedback = (videoId, uploadId, channelId) => async (dispatch) => {
  console.debug(`Upload feedback process running for video ${videoId}, upload ${uploadId}...`)
  const delayBetweenChecks = 5000;
  while (true) {
    const { data } = await getUploadById(uploadId);

    const isViewable = data.status === 'processing_viewable' || data.status === 'completed'
    const isUploaded = data.status != 'draft';
    const isProcessing = isUploaded && data.status != 'completed';
    const autogenThumbnailChoices = _uploadFeedbackAutogenThumbnailChoices(data);

    const feedback = {
      isUploaded: isUploaded,
      isViewable: isViewable,
      isProcessing: isProcessing,
      autogenThumbnailChoices: autogenThumbnailChoices,
    };
    dispatch(_setVideoUploadingFeedback(feedback));
    // dispatch({ type: aTypes.SET_VIDEO_UPLOADING_FEEDBACK, payload: feedback });
    if (isViewable && !isProcessing) {
      console.debug('Upload feedback process exiting');
      dispatch(fetchActiveChannelVideos(channelId, false));
      break
    }
    await new Promise((r) => setTimeout(r, delayBetweenChecks));
  }
}

const _uploadFeedbackAutogenThumbnailChoices = (uploadFeedbackData) => {
  if (uploadFeedbackData.autogenerated_thumbnail_choices.length > 0) {
    const thumb0 = randomItem(uploadFeedbackData.autogenerated_thumbnail_choices);
    const thumb1 = randomItem(uploadFeedbackData.autogenerated_thumbnail_choices);
    const thumb2 = randomItem(uploadFeedbackData.autogenerated_thumbnail_choices);
    return [
      [thumb0.id, thumb0.file],
      [thumb1.id, thumb1.file],
      [thumb2.id, thumb2.file],
    ];
  } else {
    return [];
  }
}

export const createChannel = (name, desc, isSynced) => async (dispatch) => {
  console.debug('action, createChannel');
  const { response, data } = await createChannelRequest(name, desc, isSynced);
  let apiErrors = {};
  if (response?.status === 400) {
    apiErrors = response?.data;
    dispatch(_setCreateChannelApiErrors(apiErrors));
  } else {
    dispatch(createToast({
      header: 'Success',
      body: 'New Channel was created!',
    }));
    dispatch(_setCreateChannelApiErrors(apiErrors));
    const allChannels = await getChannelsRequest();
    dispatch(setChannels(allChannels.data));
    dispatch(setActiveChannel(data.id));
    if (isSynced) {
      dispatch(setChannelSyncModalOpen(isSynced));
      window.location.pathname = '/channel/sync/';
    } else {
      dispatch(_setCreateChannelShowModal(false));
    }
  }
};

export const setCreateChannelShowModal = bool => async (dispatch) => {
  console.debug('action, setCreateChannelShowModal');
  dispatch(_setCreateChannelShowModal(bool));
}
