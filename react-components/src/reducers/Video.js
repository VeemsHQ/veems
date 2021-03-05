
import {
  ADD_VIDEO_LIKE,
  ADD_VIDEO_DISLIKE,
  REMOVE_VIDEO_LIKE,
  REMOVE_VIDEO_DISLIKE,
} from '../actions/ActionTypes';

export const initialState = {
  viewing: {
    videoId: null,
    likesCount: 0,
    dislikesCount: 0,
    isLiked: null,
    likesDislikesPercentage: 0,

  }
};

export default (state = initialState, action) => {
  switch (action.type) {
    case ADD_VIDEO_LIKE:
    case ADD_VIDEO_DISLIKE:
    case REMOVE_VIDEO_LIKE:
    case REMOVE_VIDEO_DISLIKE:
      return {
        ...state,
        ...{
          viewing: {
            videoId: action.videoLikeDislikeData.video_id,
            likesCount: action.videoLikeDislikeData.likes_count,
            dislikesCount: action.videoLikeDislikeData.dislikes_count,
            isLiked: action.videoLikeDislikeData.is_like,
            likesDislikesPercentage: action.videoLikeDislikeData.likesdislikes_percentage,
          }
        }
      }
    default:
      return state;
  }
};
