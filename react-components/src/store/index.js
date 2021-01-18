import { createStore, applyMiddleware, compose } from 'redux';
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage' // defaults to localStorage for web
import ReduxThunk from 'redux-thunk';

import reducer from '../reducers';

/* eslint-disable no-underscore-dangle */

const persistConfig = {
  key: 'root',
  storage,
}

const persistedReducer = persistReducer(persistConfig, reducer)

// eslint-disable-next-line no-mixed-operators
// todo: remove when not in dev. Add proper dev check.
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ &&
window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
  trace: true,
  traceLimit: 25,
}) || compose;

function configureStore() {
  const store = createStore(persistedReducer, composeEnhancers(
    applyMiddleware(ReduxThunk),
  ));
  const persistor = persistStore(store)
  return { store, persistor }
}

export default configureStore;
