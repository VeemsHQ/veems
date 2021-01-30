import * as aTypes from './ActionTypes';

/*
|--------------------------------------------------------------------------
|                          Globals Action Creators
|--------------------------------------------------------------------------
*/

export const setSessionAction = (data) => async (dispatch) => {
  dispatch({ type: aTypes.SET_SESSION, payload: data });
};

/*
|--------------------------------------------------------------------------
|                          Channels Action Creators
|--------------------------------------------------------------------------
*/

export const setActiveChannelAction = (id) => async (dispatch) => {
  dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_ID, payload: id });
  // TODO: Call get Channel Videos and set that in the state , RM subscribeToWatcher
  console.log('setActiveChannelAction');
};

export const setChannelsAction = (channels) => async (dispatch) => {
  /* When we update channels in Redux, we need to notify other components
    that the db channel may be stale.
  */
  dispatch({ type: aTypes.SET_DB_STALE, payload: true });
  dispatch({ type: aTypes.SET_CHANNELS, payload: channels });
};

export const setChannelSyncModalOpenAction = (state) => async (dispatch) => {
  dispatch({ type: aTypes.SET_CHANNEL_SYNC_MODAL_OPEN, payload: state });
};

export const setChannelsDbStaleAction = (state) => async (dispatch) => {
  dispatch({ type: aTypes.SET_DB_STALE, payload: state });
};
