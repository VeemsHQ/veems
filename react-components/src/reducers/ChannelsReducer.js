import {
  SET_ACTIVE_CHANNEL_ID,
  SET_CHANNEL_SYNC_MODAL_OPEN,
  SET_CHANNELS,
  SET_ACTIVE_CHANNEL_VIDEOS,
  SET_ACTIVE_CHANNEL_VIDEOS_LOADING,
  SET_CREATE_CHANNEL_API_ERRORS,
  SET_CREATE_CHANNEL_SHOW_MODAL,
} from '../actions/ActionTypes';

export const initialState = {
  activeChannelId: null,
  activeChannelVideos: null,
  activeChannelVideosLoading: false,
  isChannelSyncModalOpen: false,
  channels: [],
  createChannelForm: {
    apiErrors: {},
    showModal: false,
  }
};

export default (state = initialState, action) => {
  const { payload, type } = action;

  switch (type) {
    case SET_ACTIVE_CHANNEL_ID:
      return { ...state, activeChannelId: payload };
    case SET_ACTIVE_CHANNEL_VIDEOS:
      return { ...state, activeChannelVideos: payload };
    case SET_ACTIVE_CHANNEL_VIDEOS_LOADING:
      return { ...state, activeChannelVideosLoading: payload };
    case SET_CHANNEL_SYNC_MODAL_OPEN:
      return { ...state, isChannelSyncModalOpen: payload };
    case SET_CHANNELS:
      return { ...state, channels: payload };
    case SET_CREATE_CHANNEL_API_ERRORS:
      return {
        ...state,
        ...{ createChannelForm: { ...state.createChannelForm, apiErrors: payload } }
      };
    case SET_CREATE_CHANNEL_SHOW_MODAL:
      if (payload === true) {
        return {
          ...state,
          ...{ createChannelForm: { ...state.createChannelForm, showModal: payload } }
        };
      } else {
        return {
          ...state,
          ...{ createChannelForm: initialState.createChannelForm }
        };
      }
    default:
      return state;
  }
};
