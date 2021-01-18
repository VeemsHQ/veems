import {
  SET_SESSION,
} from '../actions/ActionTypes';

const initialState = {
  session: 0,
};

export default (state = initialState, action) => {
  const { payload, type } = action;

  switch (type) {
    case SET_SESSION:
      return { state, session: payload };
    default:
      return state;
  }
};
