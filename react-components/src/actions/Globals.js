import * as aTypes from './ActionTypes';

export const setSessionAction = (data) => async (dispatch) => {
  dispatch({ type: aTypes.SET_SESSION, payload: data });
};

export const createToastAction = (data) => async (dispatch) => {
  dispatch({ type: aTypes.CREATE_TOAST, payload: data });
};

export const removeToastAction = () => async (dispatch) => {
  dispatch({ type: aTypes.REMOVE_TOAST, payload: null });
};
