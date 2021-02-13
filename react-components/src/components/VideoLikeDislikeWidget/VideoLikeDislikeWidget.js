import React, { useState } from 'react';
import 'regenerator-runtime/runtime.js';

export const VideoLikeDislikeWidget = ({
  handleVideoLiked,
  handleVideoDisliked,
  handleVideoNeither,
  videoData,
}) => {
  const likeVideo = async (e) => {
    e.preventDefault();
    if (videoData.isLiked === false || videoData.isLiked === null) {
      await handleVideoLiked();
    } else {
      await handleVideoNeither();
    }
  };

  const dislikeVideo = async (e) => {
    e.preventDefault();
    if (videoData.isLiked === true || videoData.isLiked === null) {
      await handleVideoDisliked();
    } else {
      await handleVideoNeither();
    }
  };

  const getLikeControlTextColor = () => (videoData.isLiked === true ? 'text-primary' : 'text-muted');

  const getDislikeControlTextColor = () => (videoData.isLiked === false ? 'text-primary' : 'text-muted');

  const getRatioBarColor = () => {
    if (videoData.isLiked === true || videoData.isLiked === false) {
      return 'bg-primary';
    }
    return 'bg-muted';
  };

  return (
    <>
      <div className="video-menu d-inline-flex align-items-center align-middle">
        <div className="d-flex flex-column" id="video-likes-dislikes">
          <div className="d-flex flex-row">
            <a href="#" onClick={(e) => likeVideo(e)} title="I like this" className={`btn btn-sm d-flex align-items-center ${getLikeControlTextColor()}`}><i
              className="small material-icons align-middle"
            >thumb_up_alt
                                                                                                                                                          </i><span
              className="ml-2"
            >{videoData.likesCount}
                </span>
            </a>
            <a
              href="#"
              onClick={(e) => dislikeVideo(e)}
              title="I dislike this"
              className={`btn btn-sm d-flex align-items-center ${getDislikeControlTextColor()}`}
            ><i
              className="small material-icons align-middle"
            >thumb_down_alt
            </i><span
               className="ml-2"
             >{videoData.dislikesCount}
                 </span>
            </a>
          </div>
          <div className="progress likedislike-progress">
            <div
              className={`progress-bar ${getRatioBarColor()}`}
              role="progressbar"
              style={{ width: `${videoData.likesDislikesPercentage}%` }}
              aria-valuenow={videoData.likesDislikesPercentage}
              aria-valuemin="0"
              aria-valuemax="100"
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default VideoLikeDislikeWidget;
