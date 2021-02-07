import axios from 'axios';

export const API = axios.create({
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFTOKEN': window.CSRF_TOKEN,
  },
  transformRequest: [function preTransformData(data) {
    // Todo: Add some outgoing error checks to server
    return JSON.stringify(data);
  }],
  transformResponse: axios.defaults.transformResponse.concat((data) =>
    // Todo: Add some incoming error checks to server responses
    data),
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
    return err;
  }
};

export const getChannelRequest = async (channelId) => {
  try {
    const res = await API.get(`${serverURL}/api/v1/channel/${channelId}/`);
    return res;
  } catch (err) {
    return err;
  }
};

export const getAllVideosForChannelRequest = async (channelId) => {
  try {
    const res = await API.get(`${serverURL}/api/v1/video/?channel_id=${channelId}`);
    return res;
  } catch (err) {
    return err;
  }
};

export const getVideoById = async (videoId) => {
  try {
    const res = await API.get(`${serverURL}/api/v1/video/${videoId}/`);
    return res;
  } catch (err) {
    return err;
  }
};

export const getChannelsRequest = async () => {
  try {
    const res = await API.get(`${serverURL}/api/v1/channel/`);
    return res;
  } catch (err) {
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
    return err;
  }
};

export const setVideoLikeDislike = async (videoId, isLike) => {
  if (isLike == null) {
    try {
      const res = await API.delete(`${serverURL}/api/v1/video/${videoId}/likedislike/`);
      return res;
    } catch (err) {
      return err;
    }
  } else {
    const data = { is_like: isLike };
    try {
      const res = await API.post(`${serverURL}/api/v1/video/${videoId}/likedislike/`, data);
      return res;
    } catch (err) {
      return err;
    }
  }
};
