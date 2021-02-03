import {
  SET_ACTIVE_CHANNEL_ID,
  SET_CHANNEL_SYNC_MODAL_OPEN,
  SET_CHANNELS,
  SET_DB_STALE,
  SET_ACTIVE_CHANNEL_VIDEOS,
  SET_ACTIVE_CHANNEL_VIDEOS_LOADING,
} from '../actions/ActionTypes';

export const initialState = {
  activeChannelId: undefined,
  activeChannelVideos: undefined,
  activeChannelVideosLoading: false,
  isChannelSyncModalOpen: false,
  channels: [],
  isDbStale: false,
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
    case SET_DB_STALE:
      return { ...state, isDbStale: payload };
    default:
      return state;
  }
};
