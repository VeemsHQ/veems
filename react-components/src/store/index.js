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

// eslint-disable-next-line no-mixed-operators
// todo: remove when not in dev. Add proper dev check.
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ &&
window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
  trace: true,
  traceLimit: 25,
}) || compose;


/* Singleton for store to make sure we don't duplicate between components */
export class configureStore {
  static store = null;
  static persistor = null;
  static persistedReducer = null;

  static getInstance() {
    if (this.store === null || this.persistor === null)
      this.setInstance();

    const store = this.store;
    const persistor = this.persistor;
    return {store, persistor};
  }

  static setInstance() {
    this.persistedReducer = persistReducer(persistConfig, reducer)
    this.store = createStore(this.persistedReducer, composeEnhancers(
      applyMiddleware(ReduxThunk),
    ));
    this.persistor = persistStore(this.store)
  }
}

export default configureStore;
