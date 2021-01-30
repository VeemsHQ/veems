import { combineReducers } from 'redux';
import { reduxActionWatcherReducer } from 'redux-action-watcher';

import GlobalsReducer from './GlobalsReducer';
import ChannelsReducer from './ChannelsReducer';

export default combineReducers({
  globals: GlobalsReducer,
  channels: ChannelsReducer,
  reduxActionWatcherReducer,
});
