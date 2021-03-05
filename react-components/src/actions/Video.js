import {
    ADD_VIDEO_LIKE,
    ADD_VIDEO_DISLIKE,
    REMOVE_VIDEO_LIKE,
    REMOVE_VIDEO_DISLIKE,
} from './ActionTypes';
import {
    setVideoLikeDislike,
} from '../api/api';
import {
    createToastAction,
} from './Globals';

const TOAST_VIDEO_LIKED = {
    header: 'Success',
    body: 'You liked this video.',
};
const TOAST_VIDEO_DISLIKED = {
    header: 'Success',
    body: 'You disliked this video.',
};

const addVideoLikeUnsafe = videoLikeDislikeData => ({
    type: ADD_VIDEO_LIKE,
    videoLikeDislikeData
})

const addVideoDislikeUnsafe = videoLikeDislikeData => ({
    type: ADD_VIDEO_DISLIKE,
    videoLikeDislikeData
})

const removeVideoDislikeUnsafe = videoLikeDislikeData => ({
    type: REMOVE_VIDEO_DISLIKE,
    videoLikeDislikeData
})

const removeVideoLikeUnsafe = videoLikeDislikeData => ({
    type: REMOVE_VIDEO_LIKE,
    videoLikeDislikeData
})

export const toggleVideoLike = videoId => async (dispatch, getState) => {
    const isLiked = getState().video.viewing.isLiked;
    if (isLiked === false || isLiked === null) {
        // Like
        const { data } = await setVideoLikeDislike(videoId, true);
        dispatch(addVideoLikeUnsafe(data))
        dispatch(createToastAction(TOAST_VIDEO_LIKED));
    } else {
        // Remove Like
        const { data } = await setVideoLikeDislike(videoId, null);
        dispatch(removeVideoLikeUnsafe(data));
    }
}

export const toggleVideoDislike = videoId => async (dispatch, getState) => {
    const isLiked = getState().video.viewing.isLiked;
    if (isLiked === true || isLiked === null) {
        // Dislike
        const { data } = await setVideoLikeDislike(videoId, false);
        dispatch(addVideoDislikeUnsafe(data))
        dispatch(createToastAction(TOAST_VIDEO_DISLIKED));
    } else {
        // Remove Dislike
        const { data } = await setVideoLikeDislike(videoId, null);
        dispatch(removeVideoDislikeUnsafe(data));
    }
}
