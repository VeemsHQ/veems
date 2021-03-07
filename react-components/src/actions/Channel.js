import * as aTypes from './ActionTypes';
import {
    setChannelRequest,
    getAllVideosForChannelRequest,
} from '../api/api';

const _setActiveChannelId = id => ({
    type: aTypes.SET_ACTIVE_CHANNEL_ID,
    payload: id
})

const _setChannels = channels => ({
    type: aTypes.SET_CHANNELS,
    payload: channels
})

const _setActiveChannelVideosLoading = bool => ({
    type: aTypes.SET_ACTIVE_CHANNEL_VIDEOS_LOADING,
    payload: bool
})

const _setActiveChannelVideos = videos => ({
    type: aTypes.SET_ACTIVE_CHANNEL_VIDEOS,
    payload: videos
})

export const setActiveChannel = (id, callServer = true) => async (dispatch) => {
    console.debug('action, setActiveChannel');
    if (callServer) {
        setChannelRequest(id);
    }
    dispatch(_setActiveChannelId(id));
    window.SELECTED_CHANNEL_ID = id;
    if (callServer) {
        dispatch(fetchActiveChannelVideos(id));
    }
};

export const setChannels = channels => async (dispatch) => {
    console.debug('action, setChannels');
    dispatch(_setChannels(channels));
};

export const setActiveChannelVideos = videos => async (dispatch) => {
    console.debug('action, setActiveChannelVideos');
    dispatch(_setActiveChannelVideos(videos));
};

export const fetchActiveChannelVideos = (
    channelId, loadingIndication = true,
) => async (dispatch) => {
    console.debug('action, fetchActiveChannelVideos');
    if (loadingIndication) {
        dispatch(_setActiveChannelVideosLoading(true));
    }
    const { data } = await getAllVideosForChannelRequest(channelId)
    if (loadingIndication) {
        dispatch(_setActiveChannelVideosLoading(false));
    }
    dispatch(setActiveChannelVideos(data));
};
