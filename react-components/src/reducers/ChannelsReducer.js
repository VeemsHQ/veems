import {
  SET_ACTIVE_CHANNEL_ID,
  SET_SYNC_MODAL_OPEN,
  SET_CHANNELS,
} from '../actions/ActionTypes';

const initialState = {
  activeChannelID: 0,
  bSyncModalOpen: false,
  channels: [],
};

export default (state = initialState, action) => {
  const { payload, type } = action;

  switch (type) {
    case SET_ACTIVE_CHANNEL_ID:
      return { ...state, activeChannelID: payload };
    case SET_SYNC_MODAL_OPEN:
      return { ...state, bSyncModalOpen: payload };
    case SET_CHANNELS:
      return { ...state, channels: payload };
    default:
      return state;
  }
};
