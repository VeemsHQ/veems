import {
  SET_SESSION,
  REMOVE_TOAST,
  CREATE_TOAST,
} from '../actions/ActionTypes';

const initialState = {
  session: null,
  toast: null,
};

export default (state = initialState, action) => {
  const { payload, type } = action;

  switch (type) {
    case SET_SESSION:
      return { ...state, session: payload };
    case CREATE_TOAST:
      return { ...state, toast: payload };
    case REMOVE_TOAST:
      return { ...state, toast: null };
    default:
      return state;
  }
};
