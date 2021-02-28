import { combineReducers } from 'redux';
import expireReducer from 'redux-persist-expire';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // defaults to localStorage for web

import GlobalsReducer from './GlobalsReducer';
import ChannelsReducer, { initialState as ChannelsReducerInitialState } from './ChannelsReducer';
import TempReducer from './TempReducer';

const staticAssetsAuthTokenTimeout = 604800;

const rootPersistConfig = {
  key: 'root',
  storage: storage,
  blacklist: ['globals', 'channels', 'temp'],
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
const tempConfig = {
  key: 'temp',
  storage: storage,
  whitelist: [],
};

const rootReducer = combineReducers({
  globals: persistReducer(globalsConfig, GlobalsReducer),
  channels: persistReducer(channelsConfig, ChannelsReducer),
  temp: TempReducer,
});

export default persistReducer(rootPersistConfig, rootReducer);
