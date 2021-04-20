import * as aTypes from './ActionTypes';


export const createToast = (data) => async (dispatch) => {
  dispatch({ type: aTypes.CREATE_TOAST, payload: data });
};

export const removeToast = () => async (dispatch) => {
  dispatch({ type: aTypes.REMOVE_TOAST, payload: null });
};

export const destroySession = () => async (dispatch) => {
  dispatch({ type: aTypes.DESTROY_SESSION, payload: null });
};
