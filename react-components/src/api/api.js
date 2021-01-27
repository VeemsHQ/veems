import axios from 'axios';

/**
 * Axios Promise based HTTP client
 * Here we import axios and create a new configuration of it.
 * @param {string} baseURL - What url axios will use for the server requests
 * @param {number} timeout - When the server time out is set to stop responding.
 * @param {string} headers - Any additional headers we want to send infront of all server requests.
 * {@link https://github.com/axios/axios}
 */
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

// Todo: This could do with splitting into seperate apis per service

const serverURL = 'http://localhost:8000';

/**
 * API
 * Send a create channel request
 * @return Should return successful
 * @param {string} name - Channel name
 * @param {string} description - Channel description
 * @param {boolean} syncVideosInterested -
 * @param {string} language -
 * @throw Should return error
 */
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

/**
 * API
 * Send a get channel request
 * @return Should return successful
 * @param {number} channelId - Required channelId
 * @throw Should return error
 */
export const getChannelRequest = async (channelId) => {
  try {
    const res = await API.get(`${serverURL}/api/v1/channel/${channelId}/`);
    return res;
  } catch (err) {
    return err;
  }
};

/**
 * API
 * Send a get channels request
 * @return Should return successful
 * @throw Should return error
 */
export const getChannelsRequest = async () => {
  try {
    const res = await API.get(`${serverURL}/api/v1/channel/`);
    return res;
  } catch (err) {
    return err;
  }
};

/**
 * API
 * Send a set channel request
 * @return Should return successful
 * @param {number} channelId - Required channelId
 * @throw Should return error
 */
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
