import * as aTypes from './ActionTypes';

export const setSessionAction = (data) => async (dispatch) => {
  dispatch({ type: aTypes.SET_SESSION, payload: data });
};
