import {
  SET_ACTIVE_CHANNEL_ID,
  SET_SYNC_MODAL_OPEN,
  SET_CHANNELS,
  SET_DB_STALE,
} from '../actions/ActionTypes';

const initialState = {
  activeChannelID: undefined,
  isSyncModalOpen: false,
  channels: [],
  isDbStale: false,
};

export default (state = initialState, action) => {
  const { payload, type } = action;

  switch (type) {
    case SET_ACTIVE_CHANNEL_ID:
      return { ...state, activeChannelID: payload };
    case SET_SYNC_MODAL_OPEN:
      return { ...state, isSyncModalOpen: payload };
    case SET_CHANNELS:
      return { ...state, channels: payload };
    case SET_DB_STALE:
      return { ...state, isDbStale: payload };
    default:
      return state;
  }
};
