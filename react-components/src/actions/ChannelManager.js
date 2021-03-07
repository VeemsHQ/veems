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
import { _setVideoThumbnailUploading } from './Video';

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

const _setVideoDetailIsLoading = bool => ({
  type: aTypes.SET_VIDEO_DETAIL_IS_LOADING,
  payload: bool
})

const _setVideoUploadingFeedback = (videoId, feedback) => ({
  type: aTypes.SET_VIDEO_UPLOADING_FEEDBACK,
  payload: [videoId, feedback]
})

const _setVideoDetailFileSelectorIsVisible = bool => ({
  type: aTypes.SET_VIDEO_DETAIL_FILE_SELECTOR_IS_VISIBLE,
  payload: bool
})

const _setVideoDetailFileIsSelected = bool => ({
  type: aTypes.SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTED,
  payload: bool
})

const _setVideoDetailIsSaving = bool => ({
  type: aTypes.SET_VIDEO_DETAIL_IS_SAVING,
  payload: bool
})


export const setChannelSyncModalOpen = (state) => async (dispatch) => {
  console.debug('action, setChannelSyncModalOpen');
  dispatch({ type: aTypes.SET_CHANNEL_SYNC_MODAL_OPEN, payload: state });
};

const alertUserExitingPageWhileUploading = e => {
  e.preventDefault()
  const msg = 'Your uploads will be cancelled if you leave this page'
  e.returnValue = msg;
  return msg;
}

const setUserPermissionToLeavePage = (bool) => async (dispatch) => {
  console.debug('action, setUserPermissionToLeavePage');
  window.removeEventListener('beforeunload', alertUserExitingPageWhileUploading);
  if (bool === false) {
    window.addEventListener('beforeunload', alertUserExitingPageWhileUploading);
  }
}

export const updateVideoMetadata = (videoId, updatedFields) => async (dispatch) => {
  console.debug(`action, updateVideoMetadata ${videoId}`);
  dispatch(_setVideoDetailIsSaving(true));
  if (!updatedFields) {
    // If there's nothing updated, simulate the save.
    await new Promise((r) => setTimeout(r, 300));
    dispatch(createToast({
      header: 'Success',
      body: 'Your video was saved',
    }));
  } else {
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
      dispatch(fetchActiveChannelVideos(data.channel_id, true));
    }
  }
  dispatch(_setVideoDetailIsSaving(false));
}

export const openVideoDetailModal = (videoId, isFileSelectorVisible = false) => async (dispatch) => {
  console.debug('action, openVideoDetailModal');
  if (videoId) {
    dispatch(populateVideoDetail(videoId));
  }
  dispatch(_setVideoDetailFileSelectorIsVisible(isFileSelectorVisible));
  dispatch(_setVideoDetailModalOpen(true));
}

export const closeVideoDetailModal = () => async (dispatch) => {
  dispatch(_setVideoDetailModalOpen(false));
}

export const populateVideoDetail = (videoId) => async (dispatch) => {
  console.debug('action, populateVideoDetail');
  dispatch(_setVideoDetailIsLoading(true));
  const { data } = await getVideoById(videoId);
  dispatch(_setVideoDetail(data));
  dispatch(_setVideoDetailIsLoading(false));
};

export const setActiveVideoDetailThumbnailAsPrimary = (videoId, videoRenditionThumbnailId) => async (dispatch) => {
  console.debug('action, setActiveVideoDetailThumbnailAsPrimary');
  dispatch(_setVideoThumbnailUploading(true));
  const { data } = await setExistingThumbnailAsPrimary(videoId, videoRenditionThumbnailId);
  dispatch(_setVideoDetail(data));
  dispatch(_setVideoThumbnailUploading(false));
  dispatch(fetchActiveChannelVideos(data.channel_id, true));
};

const _updateUploadProgressCallback = async (videoId, percentageDone) => {
  console.debug(`Uploading ${videoId} ${percentageDone}`);
  const feedback = {
    percentageUploaded: percentageDone
  };
  store.dispatch(_setVideoUploadingFeedback(videoId, feedback));
}

const _uploadVideo = async (videoId, file, uploadPrepareResult) => {
  const chunkSize = 5 * 1024 * 1024; // 5MB
  const fileSize = file.size;
  const numParts = Math.ceil(fileSize / chunkSize)
  const uploadId = uploadPrepareResult.upload_id;
  const presignedUploadUrls = uploadPrepareResult.presigned_upload_urls;
  console.debug('Uploading video parts')
  const parts = await uploadVideoParts(
    videoId,
    presignedUploadUrls,
    file,
    numParts,
    fileSize,
    chunkSize,
    _updateUploadProgressCallback,
  )
  console.debug('Uploading video parts completed')
  await uploadComplete(uploadId, parts);
}

export const startVideoUpload = (channelId, file) => async (dispatch, getState) => {
  console.debug('action, startVideoUpload');
  dispatch(setUserPermissionToLeavePage(false));
  dispatch(_setVideoDetailFileIsSelected(true));
  const chunkSize = 5 * 1024 * 1024; // 5MB
  const filename = file.name;
  const fileSize = file.size;
  const numParts = Math.ceil(fileSize / chunkSize);

  const { response, data } = await uploadPrepare(channelId, filename, numParts);
  if (response?.status === 400) {
    console.error('UPLOAD FAILED');
  } else {
    dispatch({ type: aTypes.START_VIDEO_UPLOADING, payload: data.video_id });
    dispatch(fetchActiveChannelVideos(channelId, true));
    dispatch(populateVideoDetail(data.video_id));
    dispatch(provideUploadFeedback(data.video_id, data.upload_id, channelId));
    dispatch(_setVideoDetailFileSelectorIsVisible(false));
    await _uploadVideo(data.video_id, file, data);
    if (_haveAllVideoUploadsCompleted(getState().temp.uploadingVideos)) {
      dispatch(setUserPermissionToLeavePage(true));
    }
  }
};


const _haveAllVideoUploadsCompleted = (uploadingVideos) => {
  for (var videoId in uploadingVideos) {
    if (uploadingVideos[videoId].isUploading === true) {
      return true;
    }
  }
  return false;
}


const provideUploadFeedback = (videoId, uploadId, channelId) => async (dispatch) => {
  console.debug(`action, provideUploadFeedback, for video ${videoId}, upload ${uploadId}...`)
  const delayBetweenChecks = 5000;
  while (true) {
    console.debug(`upload feedback check, video ${videoId}, upload ${uploadId}`);
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
    dispatch(_setVideoUploadingFeedback(videoId, feedback));
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
