import * as aTypes from './ActionTypes';
import {
  getAllVideosForChannelRequest,
} from '../api/api';

/*
|--------------------------------------------------------------------------
|                          Globals Action Creators
|--------------------------------------------------------------------------
*/

export const setSessionAction = (data) => async (dispatch) => {
  dispatch({ type: aTypes.SET_SESSION, payload: data });
};

/*
|--------------------------------------------------------------------------
|                          Channels Action Creators
|--------------------------------------------------------------------------
*/

export const setActiveChannelVideosAction = (channelId) => async (dispatch) => {
  dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_VIDEOS_LOADING, payload: true });
  getAllVideosForChannelRequest(channelId).then((response) => {
    dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_VIDEOS_LOADING, payload: false });
    dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_VIDEOS, payload: response.data });
  });
};

export const setActiveChannelAction = (id) => async (dispatch) => {
  setActiveChannelVideosAction(id)(dispatch);
  dispatch({ type: aTypes.SET_ACTIVE_CHANNEL_ID, payload: id });
};

export const setChannelsAction = (channels) => async (dispatch) => {
  dispatch({ type: aTypes.SET_DB_STALE, payload: true });
  dispatch({ type: aTypes.SET_CHANNELS, payload: channels });
};

export const setChannelSyncModalOpenAction = (state) => async (dispatch) => {
  dispatch({ type: aTypes.SET_CHANNEL_SYNC_MODAL_OPEN, payload: state });
};

export const setChannelsDbStaleAction = (state) => async (dispatch) => {
  dispatch({ type: aTypes.SET_DB_STALE, payload: state });
};
