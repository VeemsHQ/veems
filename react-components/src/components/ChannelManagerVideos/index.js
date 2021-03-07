import React, { useEffect } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';

import { configureStore } from '../../store';
import {
  openVideoDetailModal,
  closeVideoDetailModal,
  setChannels,
  setActiveChannel,
  setActiveChannelVideos,
} from '../../actions/index';
import ChannelManagerVideos from './component';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  videos,
  isLoading,
  channelId,
  channels,
  setActiveChannel,
  setActiveChannelVideos,
  setChannels,
  propsSetFromHtmlContextVars,
  uploadingVideosStatuses,
  openVideoDetailModal,
  closeVideoDetailModal,
}) => {
  const callServerInitially = !propsSetFromHtmlContextVars;

  useEffect(() => {
    // If props came from HTML context we need to update Redux state to match
    // on first load.
    setActiveChannel(channelId, callServerInitially);
    setChannels(channels);
    setActiveChannelVideos(videos);
  }, [setActiveChannel, setChannels, setActiveChannelVideos])

  return (
    <ChannelManagerVideos
      videos={videos}
      channelId={channelId}
      isLoading={isLoading}
      channels={channels}
      uploadingVideosStatuses={uploadingVideosStatuses}
      onVideoDetailModalOpen={openVideoDetailModal}
      onVideoDetailModalClose={openVideoDetailModal}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    openVideoDetailModal: openVideoDetailModal,
    closeVideoDetailModal: closeVideoDetailModal,
    setChannels: setChannels,
    setActiveChannel: setActiveChannel,
    setActiveChannelVideos: setActiveChannelVideos,
  }, dispatch),
});

const mapStateToProps = (state, ownProps) => {
  let videos = [];
  let channelId = null;
  let channels = [];
  // If true then prop values came from the HTML template content.
  let propsSetFromHtmlContextVars = false;
  if (ownProps.channels && !state.channels.channels.length) {
    channels = ownProps.channels;
    propsSetFromHtmlContextVars = true;
  } else {
    channels = state.channels.channels;
  }
  if (!state.channels.activeChannelVideos) {
    videos = ownProps.videos;
    propsSetFromHtmlContextVars = true;
  } else {
    videos = state.channels.activeChannelVideos;
  }
  if (!state.channels.activeChannelId) {
    channelId = ownProps.channelId;
    propsSetFromHtmlContextVars = true;
  } else {
    channelId = state.channels.activeChannelId;
  }
  return {
    videos: videos,
    isLoading: state.channels.activeChannelVideosLoading,
    channelId: channelId,
    channels: channels,
    propsSetFromServerValues: propsSetFromHtmlContextVars,
    uploadingVideosStatuses: state.temp.uploadingVideos,
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
