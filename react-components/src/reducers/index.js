import { combineReducers } from 'redux';
import expireReducer from 'redux-persist-expire';
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // defaults to localStorage for web

import GlobalsReducer from './Global';
import ChannelsReducer, { initialState as ChannelsReducerInitialState } from './ChannelsReducer';
import TempReducer from './TempReducer';
import VideoReducer from './Video';

const staticAssetsAuthTokenTimeout = 604800;

const rootPersistConfig = {
  key: 'root',
  storage: storage,
  blacklist: ['globals', 'channels', 'temp', 'video'],
};

const globalsConfig = {
  key: 'globals',
  storage: storage,
};

const channelsConfig = {
  key: 'channels',
  transforms: [
    expireReducer('channels', {
      expireSeconds: staticAssetsAuthTokenTimeout,
      expiredState: ChannelsReducerInitialState,
      autoExpire: true,
    }),
  ],
  storage: storage,
};

const rootReducer = combineReducers({
  globals: persistReducer(globalsConfig, GlobalsReducer),
  channels: persistReducer(channelsConfig, ChannelsReducer),
  temp: TempReducer,
  video: VideoReducer,
});

export default persistReducer(rootPersistConfig, rootReducer);
