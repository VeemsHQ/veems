import * as aTypes from './ActionTypes';

/*
|--------------------------------------------------------------------------
|                          Globals Action Creators
|--------------------------------------------------------------------------
*/

/**
 * Function to set the session on the redux store.
 * @param {string} data -session ID passed to the redux store
 */
export const setSessionAction = data => async (dispatch) => {
  dispatch({ type: aTypes.SET_SESSION, payload: data });
};


/*
|--------------------------------------------------------------------------
|                          Channels Action Creators
|--------------------------------------------------------------------------
*/

/**
 * Function to set the active channel on the redux store.
 * @param {int} id - channel ID passed to the redux store
 */
export const setActiveChannelAction = id => async (dispatch) => {
  dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_ID, payload: id });
};

/**
 * Function to set the open state of the sync modal.
 * @param {boolean} state -open/closed state
 */
export const setSyncModalOpenAction = state => async (dispatch) => {
  dispatch({ type: aTypes.SET_SYNC_MODAL_OPEN, payload: state });
};