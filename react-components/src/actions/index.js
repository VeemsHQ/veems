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
