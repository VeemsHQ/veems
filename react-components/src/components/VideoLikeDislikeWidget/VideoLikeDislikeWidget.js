import React, { useState } from 'react';
import Toast from 'react-bootstrap/Toast';

import 'regenerator-runtime/runtime.js';

export const VideoLikeDislikeWidget = ({
  handleVideoLiked,
  handleVideoDisliked,
  handleVideoNeither,
  videoData,
  apiError,
  setApiError,
}) => {
  const [showToast, setShowToast] = useState(false);

  const likeVideo = async (e) => {
    e.preventDefault();
    if (videoData.isLiked === false || videoData.isLiked === null) {
      await handleVideoLiked();
      setShowToast(true);
    } else {
      await handleVideoNeither();
    }
  };

  const dislikeVideo = async (e) => {
    e.preventDefault();
    if (videoData.isLiked === true || videoData.isLiked === null) {
      await handleVideoDisliked();
      setShowToast(true);
    } else {
      await handleVideoNeither();
    }
  };

  const renderErrorToast = () => (
    <div
      aria-live="polite"
      aria-atomic="true"
      style={{
        position: 'relative',
        top: '0',
        right: '0',
        height: '2px',
        width: '200%',
        zIndex: '9999',
        overflow: 'visible',
      }}
    >
      <Toast
        style={{
          position: 'absolute',
          top: 20,
          right: 20,
        }}
        show={apiError !== ''}
        autohide
        onClose={() => setApiError('')}
      >
        <Toast.Header>
          <strong className="mr-auto">Oops</strong>
        </Toast.Header>
        <Toast.Body>{apiError}</Toast.Body>
      </Toast>
    </div>
  );

  const renderToast = () => {
    if (apiError !== false && apiError !== '') {
      return renderErrorToast();
    }
    let action;
    if (videoData.isLiked === true) {
      action = 'liked';
    } else if (videoData.isLiked === false) {
      action = 'disliked';
    } else {
      return '';
    }
    return (
      <div
        aria-live="polite"
        aria-atomic="true"
        style={{
          position: 'fixed',
          top: '0',
          right: '0',
          height: '2px',
          width: '100%',
          zIndex: '9999',
        }}
      >
        <Toast
          style={{
            position: 'absolute',
            top: 20,
            right: 20,
          }}
          show={showToast}
          autohide
          onClose={() => setShowToast(!showToast)}
        >
          <Toast.Header>
            <strong className="mr-auto">Success</strong>
          </Toast.Header>
          <Toast.Body>You {action} this video.</Toast.Body>
        </Toast>
      </div>
    );
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
      {renderToast()}
    </>
  );
};

export default VideoLikeDislikeWidget;
