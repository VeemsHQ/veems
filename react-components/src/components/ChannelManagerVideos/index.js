import React, { useEffect } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';

import { configureStore } from '../../store';
import {
  fetchActiveChannelVideosAction,
  setActiveChannelAction,
} from '../../actions/index';
import ChannelManagerVideos from './ChannelManagerVideos';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  videos,
  isLoading,
  channelId,
  fetchActiveChannelVideos,
  setActiveChannel,
}) => {
  useEffect(() => {
    setActiveChannel(channelId);
    fetchActiveChannelVideos(channelId);
  }, [channelId]);

  return (
    <ChannelManagerVideos
      videos={videos}
      channelId={channelId}
      isLoading={isLoading}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    setActiveChannel: setActiveChannelAction,
    fetchActiveChannelVideos: fetchActiveChannelVideosAction,
  }, dispatch),
});

const mapStateToProps = (state, ownProps) => {
  let videos = [];
  let channelId = null;
  if (state.channels.activeChannelVideos === null) {
    videos = ownProps.videos;
  } else {
    videos = state.channels.activeChannelVideos;
  }
  if (state.channels.activeChannelId === null) {
    channelId = ownProps.channelId;
  } else {
    channelId = state.channels.activeChannelId;
  }
  return {
    videos: videos,
    isLoading: state.channels.activeChannelVideosLoading,
    channelId: channelId,
  };
};

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const CreateChannelManagerVideos = ({
  element,
  ...params
}) => (
  ReactDOM.render(
    <PersistGate loading={null} persistor={persistor}>
      <Provider store={store}>
        <ConnectedContainer {...params} />
      </Provider>
    </PersistGate>,
    element,
  )
);
