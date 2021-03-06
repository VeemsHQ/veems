import React from 'react';

export const VideoLikeDislike = ({
  onToggleVideoLikeClicked,
  onToggleVideoDislikeClicked,
  video,
}) => {
  const likeControlTextColor = video.isLiked === true ? 'text-primary' : 'text-muted';
  const dislikeControlTextColor = video.isLiked === false ? 'text-primary' : 'text-muted';
  const ratioBarColor = (video.isLiked === true || video.isLiked === false) ? 'bg-primary' : 'bg-muted';
  return (
    <>
      <div className="video-menu d-inline-flex align-items-center align-middle">
        <div className="d-flex flex-column" id="video-likes-dislikes">
          <div className="d-flex flex-row">
            <a href="#" onClick={onToggleVideoLikeClicked} title="I like this" className={`btn btn-sm d-flex align-items-center ${likeControlTextColor}`}>
              <i className="small material-icons align-middle">thumb_up_alt</i>
              <span className="ml-2">{video.likesCount}</span>
            </a>
            <a
              href="#"
              onClick={onToggleVideoDislikeClicked}
              title="I dislike this"
              className={`btn btn-sm d-flex align-items-center ${dislikeControlTextColor}`}
            ><i
              className="small material-icons align-middle"
            >thumb_down_alt
            </i><span
                className="ml-2"
              >{video.dislikesCount}
              </span>
            </a>
          </div>
          <div className="progress likedislike-progress">
            <div
              className={`progress-bar ${ratioBarColor}`}
              role="progressbar"
              style={{ width: `${video.likesDislikesPercentage}%` }}
              aria-valuenow={video.likesDislikesPercentage}
              aria-valuemin="0"
              aria-valuemax="100"
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default VideoLikeDislike;
