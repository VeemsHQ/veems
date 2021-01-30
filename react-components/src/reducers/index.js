import { combineReducers } from 'redux';
import GlobalsReducer from './GlobalsReducer';
import ChannelsReducer from './ChannelsReducer';

export default combineReducers({
  globals: GlobalsReducer,
  channels: ChannelsReducer,
});
