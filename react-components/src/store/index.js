import { createStore, applyMiddleware, compose } from 'redux';
import ReduxThunk from 'redux-thunk';
import reducer from '../reducers';

/* eslint-disable no-underscore-dangle */

// eslint-disable-next-line no-mixed-operators
// todo: remove when not in dev. Add proper dev check.
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ &&
window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
  trace: true,
  traceLimit: 25,
}) || compose;
const store = createStore(reducer, composeEnhancers(
  applyMiddleware(ReduxThunk),
));

export default store;
