import React, { useState } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import VideoLikeDislikeWidget from './VideoLikeDislikeWidget';

import {
  createToastAction,
} from '../../actions/index';
import {
  setVideoLikeDislike,
} from '../../api/api';

const TOAST_PAYLOAD_VIDEO_LIKED = {
  header: 'Success',
  body: 'You liked this video.',
};
const TOAST_PAYLOAD_VIDEO_DISLIKED = {
  header: 'Success',
  body: 'You disliked this video.',
};

const { store, persistor } = configureStore.getInstance();

function Container(props) {
  const [videoData, setvideoData] = useState({
    likesCount: props.likesCount,
    dislikesCount: props.dislikesCount,
    // isLiked possible states: true=liked false=disliked null=neither
    isLiked: props.isLiked,
    likesDislikesPercentage: props.likesDislikesPercentage,
  });
  const updateStateFromApiResponse = async (requestPromise) => {
    const { response, data } = await requestPromise;
    if (response?.status === 403) {
      props.createToast({
        header: 'Please login',
        body: 'You need to login to do that.',
        isError: true,
      });
    } else if (response?.status > 400) {
      props.createToast({
        header: 'Oops',
        body: 'Something went wrong, please try again.',
        isError: true,
      });
    } else {
      if (data?.is_like === true) {
        props.createToast(TOAST_PAYLOAD_VIDEO_LIKED);
      } else if (data?.is_like === false) {
        props.createToast(TOAST_PAYLOAD_VIDEO_DISLIKED);
      }
      setvideoData(
        {
          likesCount: data?.likes_count,
          dislikesCount: data?.dislikes_count,
          isLiked: data?.is_like,
          likesDislikesPercentage: data?.likesdislikes_percentage,
        },
      );
      return true;
    }
    return true;
  };

  const handleVideoNeither = async () => {
    // If it was unliked/undisliked.
    await updateStateFromApiResponse(setVideoLikeDislike(props.videoId, null));
    return true;
  };

  const handleVideoLiked = async () => {
    // Is it was previously not liked/disliked or was liked and 'Like' was just clicked.
    if (videoData.isLiked === null || videoData.isLiked === false) {
      await updateStateFromApiResponse(setVideoLikeDislike(props.videoId, true));
    } else {
      await handleVideoNeither();
    }
    return true;
  };

  const handleVideoDisliked = async () => {
    // Is it was previously not liked/disliked or was liked and 'Dislike' was just clicked.
    if (videoData.isLiked === null || videoData.isLiked === true) {
      await updateStateFromApiResponse(setVideoLikeDislike(props.videoId, false));
    } else {
      await handleVideoNeither();
    }
    return true;
  };

  return (
    <VideoLikeDislikeWidget
      handleVideoLiked={handleVideoLiked}
      handleVideoDisliked={handleVideoDisliked}
      handleVideoNeither={handleVideoNeither}
      videoData={videoData}
    />
  );
}

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    createToast: createToastAction,
  }, dispatch),
});

const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

export const CreateVideoLikeDislikeWidget = ({
  element,
  ...params
}) => (
  ReactDOM.render(
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <ConnectedContainer {...params} />
      </PersistGate>
    </Provider>,
    element,
  )
);
