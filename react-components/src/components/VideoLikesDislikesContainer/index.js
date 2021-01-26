import React, { useState } from 'react';
import ReactDOM from 'react-dom'

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { configureStore } from '../../store';
import { PersistGate } from 'redux-persist/integration/react'

import VideoLikesDislikesContainer from './VideoLikesDislikesContainer';

import {
  setSyncModalOpenAction,
  setActiveChannelAction,
  setChannelsAction,
} from '../../actions/index';

import {
  setVideoLikeDislike,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

// TODO: error when  not logged in
// TODO: Sign in btn doesn't work when toast on page

function Container(props) {
  const [likesCount, setLikesCount] = useState(props.likesCount);
  const [dislikesCount, setDislikesCount] = useState(props.dislikesCount);
  // isLiked possible states: true=liked false=disliked null=neither
  const [isLiked, setIsLiked] = useState(props.isLiked);
  const [likesDislikesPercentage, setLikesDislikesPercentage] = useState(props.likesDislikesPercentage);

  const updateStateFromApiResponse =  async (response) => {
    setLikesCount(response.data.likes_count)
    setDislikesCount(response.data.dislikes_count)
    setIsLiked(response.data.is_like);
    setLikesDislikesPercentage(response.data.likesdislikes_percentage);
  }

  const handleVideoNeither = async () => {
    const response = await setVideoLikeDislike(props.videoId, null);
    await updateStateFromApiResponse(response);
    return true
  }

  const handleVideoLiked = async () => {
    if (isLiked == null || isLiked == false) {
      const response = await setVideoLikeDislike(props.videoId, true);
      await updateStateFromApiResponse(response);
    } else {
      await handleVideoNeither()
    }
    return true
  }

  const handleVideoDisliked = async () => {
    if (isLiked == null || isLiked == true) {
      const response = await setVideoLikeDislike(props.videoId, false);
      await updateStateFromApiResponse(response);
    } else {
      await handleVideoNeither()
    }
    return true
  }

  return (
    <VideoLikesDislikesContainer
      handleVideoLiked={handleVideoLiked}
      handleVideoDisliked={handleVideoDisliked}
      handleVideoNeither={handleVideoNeither}
      dislikesCount={dislikesCount}
      likesCount={likesCount}
      isLiked={isLiked}
      likesDislikesPercentage={likesDislikesPercentage}
    />
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({
      setSyncModalOpen: setSyncModalOpenAction,
      setActiveChannel: setActiveChannelAction,
      setChannels: setChannelsAction,
    }, dispatch),
  };
};

const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

export const CreateVideoLikesDislikesContainer = ({
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

