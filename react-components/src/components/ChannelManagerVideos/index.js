import React, { useEffect } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';

import { configureStore } from '../../store';
import {
  openVideoDetailModal,
  closeVideoDetailModal,
} from '../../actions/index';
import ChannelManagerVideos from './component';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  videos,
  isLoading,
  channelId,
  channels,
  uploadingVideosStatuses,
  openVideoDetailModal,
  closeVideoDetailModal,
}) => {

  // useEffect(() => {
  // TODO: launch check loop for processing videos
  // }, [])


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
  }, dispatch),
});

const mapStateToProps = (state, ownProps) => {
  let videos = [];
  let channelId = null;
  let channels = [];
  if (ownProps.channels && !state.channels.channels.length) {
    channels = ownProps.channels;
  } else {
    channels = state.channels.channels;
  }
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
    channels: channels,
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
