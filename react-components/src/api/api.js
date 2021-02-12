import axios from 'axios';
import { configureStore } from '../store';
import { MSG_SERVER_ERROR } from '../constants';
import {
  createToastAction,
} from '../actions/index';

const { store } = configureStore.getInstance();

const handleError = (error) => {
  if (error.response.status >= 500) {
    store.dispatch(createToastAction({
      header: 'Oops',
      body: MSG_SERVER_ERROR,
      isError: true,
    }));
  }
};

export const API = axios.create({
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFTOKEN': window.CSRF_TOKEN,
  },
  transformRequest: [function preTransformData(data) {
    return JSON.stringify(data);
  }],
  transformResponse: axios.defaults.transformResponse.concat((data) => data),
});
const API_MULTIPART = axios.create({
  timeout: 5000,
  headers: {
    'Content-Type': 'multipart/form-data',
    'X-CSRFTOKEN': window.CSRF_TOKEN,
  },
  transformResponse: axios.defaults.transformResponse.concat((data) => data),
});

const serverURL = window.API_BASE_URL;

export const createChannelRequest = async (name, description, syncVideosInterested) => {
  const data = {
    name,
    description,
    sync_videos_interested: syncVideosInterested,
    language: 'en',
    is_selected: true,
  };
  try {
    const res = await API.post(`${serverURL}/api/v1/channel/`, data);
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const getChannelRequest = async (channelId) => {
  try {
    const res = await API.get(`${serverURL}/api/v1/channel/${channelId}/`);
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const getAllVideosForChannelRequest = async (channelId) => {
  try {
    const res = await API.get(`${serverURL}/api/v1/video/?channel_id=${channelId}`);
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const getVideoById = async (videoId) => {
  try {
    const res = await API.get(`${serverURL}/api/v1/video/${videoId}/`);
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const updateVideo = async (videoId, data) => {
  try {
    const res = await API.put(`${serverURL}/api/v1/video/${videoId}/`, data);
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const setExistingThumbnailAsPrimary = async (videoId, videoRenditionThumbnailId) => {
  try {
    const res = await API.post(`${serverURL}/api/v1/video/${videoId}/thumbnail/${videoRenditionThumbnailId}/`);
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const updateVideoCustomThumbnail = async (videoId, thumbFile) => {
  const formData = new FormData();
  formData.append('file', thumbFile);
  try {
    const res = await API_MULTIPART.post(
      `${serverURL}/api/v1/video/${videoId}/thumbnail/`, formData,
    );
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const getChannelsRequest = async () => {
  try {
    const res = await API.get(`${serverURL}/api/v1/channel/`);
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const setChannelRequest = async (channelId) => {
  const data = {
    is_selected: true,
  };
  try {
    const res = await API.put(`${serverURL}/api/v1/channel/${channelId}/`, data);
    return res;
  } catch (err) {
    handleError(err);
    return err;
  }
};

export const setVideoLikeDislike = async (videoId, isLike) => {
  if (isLike == null) {
    try {
      const res = await API.delete(`${serverURL}/api/v1/video/${videoId}/likedislike/`);
      return res;
    } catch (err) {
      handleError(err);
      return err;
    }
  } else {
    const data = { is_like: isLike };
    try {
      const res = await API.post(`${serverURL}/api/v1/video/${videoId}/likedislike/`, data);
      return res;
    } catch (err) {
      handleError(err);
      return err;
    }
  }
};
