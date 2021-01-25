
import React, { useState } from 'react';

import "regenerator-runtime/runtime.js";

export const VideoLikesDislikesContainer = ({
  onCreateChannel,
}) => {
  const [likesCount, likeVideo] = useState(0);
  const [dislikesCount, dislikeVideo] = useState(0);
  const [isLiked, setAsLiked] = useState(false);

  const doLikeVideo = async () => {
    // const isChannelCreated = await onCreateChannel(channelName, channelDescription, isChannelSynced);
    // if (isChannelCreated) {
    //   setShowChannelModal(false);
    //   // Show toast success.
    //   setShowToast(true);
    // } else {
    //   setChannelWarning('Sorry, it looks like something has gone wrong.');
    // }
    setAsLiked(true);
  };

  return (
    <>
      <div className="video-menu d-inline-flex align-items-center align-middle">
        <div className="d-flex flex-column" id="video-likes-dislikes">
          <div className="d-flex flex-row">
            <a href="#" onClick={() => doLikeVideo()} title="I like this" className="btn btn-sm text-muted d-flex align-items-center"><i
              className="small material-icons align-middle">thumb_up_alt</i><span
                className="ml-2">{likesCount}</span></a>
            <a href="#" title="I dislike this"
              className="btn btn-sm text-muted d-flex align-items-center"><i
                className="small material-icons align-middle">thumb_down_alt</i><span
                  className="ml-2">{dislikesCount}</span></a>
          </div>
          <div className="progress likedislike-progress">
            {/* TODO width */}
            <div className="progress-bar bg-muted" role="progressbar" style={{width: '50%'}} aria-valuenow="50"
              aria-valuemin="0" aria-valuemax="100"></div>
          </div>
        </div>
        </div>
    </>
  );
};

export default VideoLikesDislikesContainer;


