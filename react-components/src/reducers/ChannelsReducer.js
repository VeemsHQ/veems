import {
  SET_ACTIVE_CHANNEL_ID,
  SET_CHANNEL_SYNC_MODAL_OPEN,
  SET_CHANNELS,
  SET_DB_STALE,
  SET_ACTIVE_CHANNEL_VIDEOS,
  SET_ACTIVE_CHANNEL_VIDEOS_LOADING,
} from '../actions/ActionTypes';

export const initialState = {
  activeChannelId: null,
  activeChannelVideos: null,
  activeChannelVideosLoading: false,
  isChannelSyncModalOpen: false,
  channels: [],
  isDbStale: false,
};

export default (state = initialState, action) => {
  const { payload, type } = action;
  let newState = null;

  switch (type) {
    case SET_ACTIVE_CHANNEL_ID:
      console.debug('Reduce SET_ACTIVE_CHANNEL_ID');
      return { ...state, activeChannelId: payload };
    case SET_ACTIVE_CHANNEL_VIDEOS:
      console.debug('Reduce SET_ACTIVE_CHANNEL_VIDEOS');
      return { ...state, activeChannelVideos: payload };
    case SET_ACTIVE_CHANNEL_VIDEOS_LOADING:
      console.debug('Reduce SET_ACTIVE_CHANNEL_VIDEOS_LOADING');
      return { ...state, activeChannelVideosLoading: payload };
    case SET_CHANNEL_SYNC_MODAL_OPEN:
      console.debug('Reduce SET_CHANNEL_SYNC_MODAL_OPEN');
      return { ...state, isChannelSyncModalOpen: payload };
    case SET_CHANNELS:
      console.debug('Reduce SET_CHANNELS');
      return { ...state, channels: payload };
    case SET_DB_STALE:
      console.debug('Reduce SET_DB_STALE');
    default:
      return state;
  }
};
