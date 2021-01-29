import React, { useState } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import VideoLikeDislikeWidget from './VideoLikeDislikeWidget';

import {
  setVideoLikeDislike,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

function Container(props) {
  const [apiError, setApiError] = useState('');
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
      setApiError('You need to login to do that.');
    } else if (response?.status > 400) {
      setApiError('Something went wrong, please try again.');
    } else {
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
      apiError={apiError}
      setApiError={setApiError}
    />
  );
}

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
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
