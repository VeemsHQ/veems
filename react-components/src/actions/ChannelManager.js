import * as aTypes from './ActionTypes';
import {
  getAllVideosForChannelRequest,
  uploadVideoParts,
  uploadComplete,
  uploadPrepare,
  getVideoById,
  setExistingThumbnailAsPrimary,
  updateVideo,
} from '../api/api';
import { MSG_CORRECT_FORM_ERRORS } from '../constants';
import { configureStore } from '../store';

const { store } = configureStore.getInstance();

export const fetchActiveChannelVideosAction = (
  channelId, loadingIndication = true,
) => async (dispatch) => {
  if (loadingIndication) {
    dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_VIDEOS_LOADING, payload: true });
  }
  const { data } = await getAllVideosForChannelRequest(channelId)
  if (loadingIndication) {
    dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_VIDEOS_LOADING, payload: false });
  }
  dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_VIDEOS, payload: data });
};

export const setActiveChannelAction = (id) => async (dispatch) => {
  fetchActiveChannelVideosAction(id)(dispatch);
  dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_ID, payload: id });
};

export const setChannelsAction = (channels) => async (dispatch) => {
  dispatch({ type: aTypes.SET_DB_STALE, payload: true });
  dispatch({ type: aTypes.SET_CHANNELS, payload: channels });
};

export const setChannelSyncModalOpenAction = (state) => async (dispatch) => {
  dispatch({ type: aTypes.SET_CHANNEL_SYNC_MODAL_OPEN, payload: state });
};

export const setChannelsDbStaleAction = (state) => async (dispatch) => {
  dispatch({ type: aTypes.SET_DB_STALE, payload: state });
};

const TOAST_PAYLOAD_VIDEO_DETAIL_SAVED = {
  header: 'Success',
  body: 'Your video was saved',
};
const TOAST_PAYLOAD_VIDEO_DETAIL_BAD_INPUT = {
  header: 'Oops',
  body: MSG_CORRECT_FORM_ERRORS,
  isError: true,
};

export const updateActiveVideoDetailMetadataAction = (videoId, updatedFields) => async (dispatch) => {
  const { response, data } = await updateVideo(videoId, updatedFields);
  if (response?.status === 400) {
    // setApiErrors(response?.data);
    dispatch({ type: aTypes.CREATE_TOAST, payload: TOAST_PAYLOAD_VIDEO_DETAIL_BAD_INPUT });
  } else {
    dispatch({ type: aTypes.CREATE_TOAST, payload: TOAST_PAYLOAD_VIDEO_DETAIL_SAVED });
    // setApiErrors(null);
    console.log(11);
    dispatch({ type: aTypes.SET_ACTIVE_VIDEO_DETAIL_DATA, payload: data });
    fetchActiveChannelVideosAction(data.channel_id, false)(dispatch);
  }
}

export const openVideoDetailModalAction = (videoId) => async (dispatch) => {
  console.log(`openVideoDetailModalAction: ${videoId}`);
  setActiveVideoDetailDataAction(videoId)(dispatch);
  dispatch({ type: aTypes.SET_VIDEO_DETAIL_MODAL_OPEN, payload: true });
}

export const closeVideoDetailModalAction = () => async (dispatch) => {
  dispatch({ type: aTypes.SET_VIDEO_DETAIL_MODAL_OPEN, payload: false });
}

export const setActiveVideoDetailDataAction = (videoId) => async (dispatch) => {
  const { data } = await getVideoById(videoId);
  dispatch({ type: aTypes.SET_ACTIVE_VIDEO_DETAIL_DATA, payload: data });
};

export const setActiveVideoDetailThumbnailAsPrimaryAction = (videoId, videoRenditionThumbnailId) => async (dispatch) => {
  const { data } = await setExistingThumbnailAsPrimary(videoId, videoRenditionThumbnailId);
  fetchActiveChannelVideosAction(data.channel_id, false)(dispatch);
  dispatch({ type: aTypes.SET_ACTIVE_VIDEO_DETAIL_DATA, payload: data });
};

export const setFileSelectorVisibleAction = (bool) => async (dispatch) => {
  dispatch({ type: aTypes.SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTOR_VISIBLE, payload: bool });
}

const _updateUploadProgress = async (percentageDone) => {
  console.debug(`Upload progress updated: ${percentageDone}`);
  const feedback = {
    percentageUploaded: percentageDone
  };
  store.dispatch({ type: aTypes.SET_VIDEO_UPLOADING_FEEDBACK, payload: feedback });
  // TODO: get the video
}

const _uploadVideo = async (file, uploadPrepareResult) => {
  // updateUploadProgress(0);

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

export const startVideoUploadAction = (channelId, file) => async (dispatch) => {

  // const file = acceptedFiles[0]
  const chunkSize = 5 * 1024 * 1024; // 5MB
  const filename = file.name;
  const fileSize = file.size;
  const numParts = Math.ceil(fileSize / chunkSize);

  const { response, data } = await uploadPrepare(channelId, filename, numParts);
  if (response?.status === 400) {
    console.error('UPLOAD FAILED');
  } else {
    dispatch({ type: aTypes.START_VIDEO_UPLOADING, payload: data.video_id });
    provideUploadFeedback(data.video_id, data.upload_id)(dispatch);
    setActiveVideoDetailDataAction(data.video_id)(dispatch);
    await _uploadVideo(file, data);
  }
};

const provideUploadFeedback = (videoId, uploadId) => async (dispatch) => {
  while (true) {
    console.log('######## Feedback loop');
    const { data } = await getVideoById(videoId);
    console.log(data.is_viewable);
    const feedback = {
      isViewable: data.is_viewable
    };
    dispatch({ type: aTypes.SET_VIDEO_UPLOADING_FEEDBACK, payload: feedback });
    if (data.is_viewable) {
      console.log('Feedback exit ##########');
      break
    }
    await new Promise((r) => setTimeout(r, 3000));
  }

}
