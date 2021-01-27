import React, { useState } from 'react';
import Toast from 'react-bootstrap/Toast';

import "regenerator-runtime/runtime.js";

export const VideoLikeDislikeWidget = ({
  handleVideoLiked,
  handleVideoDisliked,
  handleVideoNeither,
  likesCount,
  dislikesCount,
  isLiked,
  likesDislikesPercentage,
  apiError,
  setApiError,
}) => {
  const [showToast, setShowToast] = useState(false);

  const likeVideo = async (e) => {
    e.preventDefault();
    if (isLiked == false || isLiked == null) {
      await handleVideoLiked();
      setShowToast(true);
    } else {
      await handleVideoNeither();
    }
  };

  const dislikeVideo = async (e) => {
    e.preventDefault();
    if (isLiked == true || isLiked == null) {
      await handleVideoDisliked();
      setShowToast(true);
    } else {
      await handleVideoNeither();
    }
  };

  const renderErrorToast = () => {
    return (
      <div
        aria-live="polite"
        aria-atomic="true"
        style={{
          position: 'fixed',
          top: '0',
          right: '0',
          padding: '20px',
          margin: '20px',
          width: '100%',
          zIndex: '9999',
        }}
      >
        <Toast
          style={{
            position: 'absolute',
            top: 0,
            right: 0,
          }}
          show={apiError != ''}
          autohide={true}
          onClose={() => setApiError('')}
        >
          <Toast.Header>
            <strong className="mr-auto">Error</strong>
          </Toast.Header>
          <Toast.Body>{apiError}</Toast.Body>
        </Toast>
      </div>
    )
  }

  const renderToast = () => {
    if (apiError !== false) {
      return renderErrorToast();
    }
    let action;
    if (isLiked === true) {
      action = 'liked';
    } else if (isLiked === false) {
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
          padding: '20px',
          margin: '20px',
          width: '100%',
          zIndex: '9999',
        }}
      >
        <Toast
          style={{
            position: 'absolute',
            top: 0,
            right: 0,
          }}
          show={showToast}
          autohide={true}
          onClose={() => setShowToast(!showToast)}
        >
          <Toast.Header>
            <strong className="mr-auto">Success</strong>
          </Toast.Header>
          <Toast.Body>You {action} this video.</Toast.Body>
        </Toast>
      </div>
    )
  }

  const getLikeControlTextColor = () => {
    if (isLiked === true) {
      return 'text-primary';
    } else {
      return 'text-muted';
    }
  }

  const getDislikeControlTextColor = () => {
    if (isLiked === false) {
      return 'text-primary';
    } else {
      return 'text-muted';
    }
  }

  const getRatioBarColor = () => {
    if (isLiked === true || isLiked === false) {
      return 'bg-primary';
    } else {
      return 'bg-muted';
    }
  }

  return (
    <>
      <div className="video-menu d-inline-flex align-items-center align-middle">
        <div className="d-flex flex-column" id="video-likes-dislikes">
          <div className="d-flex flex-row">
            <a href="#" onClick={(e) => likeVideo(e)} title="I like this" className={"btn btn-sm d-flex align-items-center " + getLikeControlTextColor()}><i
              className="small material-icons align-middle">thumb_up_alt</i><span
                className="ml-2">{likesCount}</span></a>
            <a href="#" onClick={(e) => dislikeVideo(e)} title="I dislike this"
              className={"btn btn-sm d-flex align-items-center " + getDislikeControlTextColor()}><i
                className="small material-icons align-middle">thumb_down_alt</i><span
                  className="ml-2">{dislikesCount}</span></a>
          </div>
          <div className="progress likedislike-progress">
            <div className={"progress-bar " + getRatioBarColor()} role="progressbar" style={{ width: `${likesDislikesPercentage}%` }} aria-valuenow={likesDislikesPercentage}
              aria-valuemin="0" aria-valuemax="100"></div>
          </div>
        </div>
      </div>
      {renderToast()}
    </>
  );
};

export default VideoLikeDislikeWidget;


