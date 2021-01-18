import {
  SET_ACTIVE_CHANNEL_ID,
  SET_SYNC_MODAL_OPEN,
} from '../actions/ActionTypes';

const initialState = {
  activeChannelID: 0,
  bSyncModalOpen: false,
};

export default (state = initialState, action) => {
  const { payload, type } = action;

  switch (type) {
    case SET_ACTIVE_CHANNEL_ID:
      return { ...state, session: payload };
    case SET_SYNC_MODAL_OPEN:
      return { ...state, bSyncModalOpen: payload };
    default:
      return state;
  }
};
