import {
    ADD_VIDEO_LIKE,
    ADD_VIDEO_DISLIKE,
    REMOVE_VIDEO_LIKE,
    REMOVE_VIDEO_DISLIKE,
    SET_VIDEO_THUMBNAIL_UPLOADING,
} from './ActionTypes';
import {
    setVideoLikeDislike,
    updateVideoCustomThumbnail,
} from '../api/api';
import {
    createToast,
} from './Global';
import {
    setVideoDetail,
} from './ChannelManager';
import {
    fetchActiveChannelVideos,
} from './Channel';

const TOAST_VIDEO_LIKED = {
    header: 'Success',
    body: 'You liked this video.',
};
const TOAST_VIDEO_DISLIKED = {
    header: 'Success',
    body: 'You disliked this video.',
};

const _addVideoLike = videoLikeDislikeData => ({
    type: ADD_VIDEO_LIKE,
    videoLikeDislikeData
})

const _addVideoDislike = videoLikeDislikeData => ({
    type: ADD_VIDEO_DISLIKE,
    videoLikeDislikeData
})

const _removeVideoDislike = videoLikeDislikeData => ({
    type: REMOVE_VIDEO_DISLIKE,
    videoLikeDislikeData
})

const _removeVideoLike = videoLikeDislikeData => ({
    type: REMOVE_VIDEO_LIKE,
    videoLikeDislikeData
})

export const _setVideoThumbnailUploading = bool => ({
    type: SET_VIDEO_THUMBNAIL_UPLOADING,
    payload: bool
})

export const toggleVideoLike = (videoId, isLiked) => async (dispatch) => {
    console.debug('action, toggleVideoLike');
    if (isLiked === false || isLiked === null) {
        // Like
        const { data } = await setVideoLikeDislike(videoId, true);
        dispatch(_addVideoLike(data))
        dispatch(createToast(TOAST_VIDEO_LIKED));
    } else {
        // Remove Like
        const { data } = await setVideoLikeDislike(videoId, null);
        dispatch(_removeVideoLike(data));
    }
}

export const toggleVideoDislike = (videoId, isLiked) => async (dispatch) => {
    console.debug('action, toggleVideoDislike');
    if (isLiked === true || isLiked === null) {
        // Dislike
        const { data } = await setVideoLikeDislike(videoId, false);
        dispatch(_addVideoDislike(data))
        dispatch(createToast(TOAST_VIDEO_DISLIKED));
    } else {
        // Remove Dislike
        const { data } = await setVideoLikeDislike(videoId, null);
        dispatch(_removeVideoDislike(data));
    }
}

export const setVideoCustomThumbnail = (channelId, videoId, file) => async (dispatch) => {
    console.debug('action, setVideoCustomThumbnail');
    dispatch(_setVideoThumbnailUploading(true));
    await updateVideoCustomThumbnail(videoId, file);
    dispatch(setVideoDetail(videoId));
    dispatch(_setVideoThumbnailUploading(false));
    dispatch(fetchActiveChannelVideos(channelId, false));
    dispatch(createToast({
        header: 'Success',
        body: 'Your video was saved',
    }));
}
