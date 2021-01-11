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
  headers: { 'Content-Type': 'text/plain' },
  transformRequest: [function preTransformData(data) {
    // Todo: Add some outgoing error checks to server
    return JSON.stringify(data);
  }],
  transformResponse: axios.defaults.transformResponse.concat(function (data) {
    // Todo: Add some incoming error checks to server responses
    return data;
  })
});

// Todo: This could do with splitting into seperate apis per service

const getServerURL = async () => {
  // todo.
  return 'http://localhost:8000/';
}

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
const createChannel = async ( name, description, syncVideosInterested, language ) => {
  const data = {
    name,
    description,
    sync_videos_interested: syncVideosInterested,
    language,
  };
  try {
    const res = await API.post(`${await getServerURL()}'/api/v1/channel/`, data);
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
const getChannel = async ( channelId ) => {
  const data = {
    id : channelId,
  };
  
  try {
    const res = await API.get(`${await getServerURL()}/api/v1/channel/${channelId}`);
    return res;
  } catch (err) {
    return err;
  }
};

export {
  createChannel,
  getChannel,
};
