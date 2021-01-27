import React, { useState } from 'react';
import ReactDOM from 'react-dom'

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { configureStore } from '../../store';
import { PersistGate } from 'redux-persist/integration/react'

import VideoLikeDislikeWidget from './VideoLikeDislikeWidget';

import {
  setVideoLikeDislike,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

// TODO: Sign in btn doesn't work when toast on page

function Container(props) {
  const [apiError, setApiError] = useState('');
  const [likesCount, setLikesCount] = useState(props.likesCount);
  const [dislikesCount, setDislikesCount] = useState(props.dislikesCount);
  // isLiked possible states: true=liked false=disliked null=neither
  const [isLiked, setIsLiked] = useState(props.isLiked);
  const [likesDislikesPercentage, setLikesDislikesPercentage] = useState(props.likesDislikesPercentage);

  const updateStateFromApiResponse = async (requestPromise) => {
    const { response, data } = await requestPromise;
    if (response?.status === 403) {
      setApiError('You need to login to do that.')
    } else if (response?.status > 400) {
      setApiError('Something went wrong, please try again.')
    } else {
      setLikesCount(data?.likes_count)
      setDislikesCount(data?.dislikes_count)
      setIsLiked(data?.is_like);
      setLikesDislikesPercentage(data?.likesdislikes_percentage);
      return true;
    }
  }

  const handleVideoNeither = async () => {
    await updateStateFromApiResponse(setVideoLikeDislike(props.videoId, null));
    return true
  }

  const handleVideoLiked = async () => {
    if (isLiked === null || isLiked === false) {
      await updateStateFromApiResponse(setVideoLikeDislike(props.videoId, true));
    } else {
      await handleVideoNeither()
    }
    return true
  }

  const handleVideoDisliked = async () => {
    if (isLiked === null || isLiked === true) {
      await updateStateFromApiResponse(setVideoLikeDislike(props.videoId, false));
    } else {
      await handleVideoNeither()
    }
    return true
  }

  return (
    <VideoLikeDislikeWidget
      handleVideoLiked={handleVideoLiked}
      handleVideoDisliked={handleVideoDisliked}
      handleVideoNeither={handleVideoNeither}
      dislikesCount={dislikesCount}
      likesCount={likesCount}
      isLiked={isLiked}
      likesDislikesPercentage={likesDislikesPercentage}
      apiError={apiError}
      setApiError={setApiError}
    />
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({
    }, dispatch),
  };
};

const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

export const CreateVideoLikeDislikeWidget = ({
  element,
  ...params
}) => {
  return (
    ReactDOM.render(
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <ConnectedContainer {...params} />
        </PersistGate>
      </Provider>,
      element
    )
  );
};

