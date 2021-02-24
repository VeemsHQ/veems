import { createStore, applyMiddleware, compose } from 'redux';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // defaults to localStorage for web
import ReduxThunk from 'redux-thunk';
import expireReducer from 'redux-persist-expire';

import reducer from '../reducers';
import { initialState as ChannelsReducerInitialState } from '../reducers/ChannelsReducer';

// 1 week. Must match IMAGEKIT_CACHE_TIMEOUT, AWS_QUERYSTRING_EXPIRE in settings.py
const staticAssetsAuthTokenTimeout = 604800;
/* eslint-disable no-underscore-dangle */
// const blacklistFilter = createBlacklistFilter(
//   'channels',
//   // Clear this data between page reloads.
//   [
//     'activeVideoDetailData',
//     'uploadingVideosFeedback',
//     'uploadingVideos',
//     'isVideoFileSelectorVisible',
//     'isVideoDetailModalOpen',
//     'displayUploadModal',
//   ]
// );
const persistConfig = {
  key: 'root',
  storage,
  transforms: [
    expireReducer('channels', {
      expireSeconds: staticAssetsAuthTokenTimeout,
      expiredState: ChannelsReducerInitialState,
      autoExpire: true,
    }),
  ],
};

// todo: remove when not in dev. Add proper dev check.
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
  // eslint-disable-next-line no-mixed-operators
  && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
    trace: true,
    traceLimit: 25,
    // eslint-disable-next-line no-mixed-operators
  }) || compose;


/* Singleton for store to make sure we don't duplicate between components */
export class configureStore {
  static store = null;

  static persistor = null;

  static persistedReducer = null;

  static getInstance() {
    if (this.store === null || this.persistor === null) this.setInstance();

    const { store } = this;
    const { persistor } = this;
    return { store, persistor };
  }

  static setInstance() {
    this.persistedReducer = persistReducer(persistConfig, reducer);
    this.store = createStore(this.persistedReducer, composeEnhancers(
      applyMiddleware(ReduxThunk),
    ));
    this.store.dispatch({
      type: 'RESET_DATA_ON_PAGE_LOAD',
    })
    this.persistor = persistStore(this.store);
  }
}

export default configureStore;
