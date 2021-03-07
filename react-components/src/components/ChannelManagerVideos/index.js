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
  provideUploadFeedback,
} from '../../actions/index';
import ChannelManagerVideos from './component';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  videos,
  uploadsProcessing,
  isLoading,
  channelId,
  channels,
  setActiveChannel,
  setActiveChannelVideos,
  provideUploadFeedback,
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

    // uploadsProcessing have items if you upload a video and reload
    // the page before it's done processing.
    // We use this list of uploads to re-trigger the background API polling
    // of the video upload feedback/status.
    // This gives the live updates on the Channel Videos Page for the
    // status of the processing of the videos.
    for (let upload of uploadsProcessing) {
      provideUploadFeedback(
        upload.video_id,
        upload.id,
        upload.channel_id,
      )
    }

  }, [setActiveChannel, setChannels, setActiveChannelVideos, provideUploadFeedback])

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
    provideUploadFeedback: provideUploadFeedback,
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
    uploadsProcessing: ownProps.uploadsProcessing,
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
