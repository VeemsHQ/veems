import { combineReducers } from 'redux';
import GlobalsReducer from './GlobalsReducer';

export default combineReducers({
  globals: GlobalsReducer,
});
